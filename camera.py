import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
from data_helper import calculateRGBdiff
import os
import datetime
import imutils
from imutils.video import VideoStream
from imutils.io import TempFile
import random

from sendemail import *
from sendvps import *
from sendtelegram import *


actionlist = []
recordlist = []

dim = (224,224)
n_sequence = 8
n_channels = 3
n_output = 3
weights_path = 'weight-100-0.97-0.98.hdf5'



model = load_model(weights_path)

frame_window = np.empty((0, *dim, n_channels))

RUN_STATE = 0
WAIT_STATE = 1
SET_NEW_ACTION_STATE = 2
state = RUN_STATE # 
previous_action = -1
text_show = 'no action'


class_text = [
'1 Vo tay',
'2 Di bo',
'3 Uong nuoc'
]

fps = 4
width = 864
height = 640
video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")

cap = cv2.VideoCapture(0)
ret = cap.set(3, 864)
ret = cap.set(4, 480)

video_file_count = 0
start_time = time.time()
start = time.time()
namevideo = str(datetime.datetime.now())
video_file = os.path.join('output', namevideo + ".avi")
print("Capture video saved location : {}".format(video_file))

video_writer = cv2.VideoWriter(
    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
)


while(cap.isOpened()):
    ret, frame = cap.read()
    start_time_ = time.time()
    if ret == True:
        
        new_f = cv2.resize(frame, dim)
        new_f = new_f/255.0
        new_f_rs = np.reshape(new_f, (1, *new_f.shape))
        frame_window = np.append(frame_window, new_f_rs, axis=0)
        
        if frame_window.shape[0] >= n_sequence:
            frame_window_dif = calculateRGBdiff(frame_window.copy())
            frame_window_new = frame_window_dif.reshape(1, *frame_window_dif.shape)            
            output = model.predict(frame_window_new)[0]           
            predict_ind = np.argmax(output)
            
            
            if output[predict_ind] < 0.80:
                new_action = -1
            else:
                new_action = predict_ind

          
            if state == RUN_STATE:
                if new_action != previous_action: # action change
                    state = WAIT_STATE
                    start_time = time.time()     
                else:
                    if previous_action == -1:
                        text_show = 'no action'                                              
                    else:
                        text_show = "{: <22}  {:.2f} ".format(class_text[previous_action],
                                    output[previous_action] )
                      

            elif state == WAIT_STATE:
                dif_time = time.time() - start_time
                if dif_time > 0.5:
                    state = RUN_STATE
                    previous_action = new_action


            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, text_show, (10,450), font, 0.8, (0, 225, 0), 2, cv2.LINE_AA)            
            cv2.putText(frame, ("%s %s:%s:%s"%(str(datetime.datetime.now().date()),str(datetime.datetime.now().hour),str(datetime.datetime.now().minute),str(datetime.datetime.now().second))), (10,50), font, 0.7, (0, 225, 0), 2, cv2.LINE_AA)
            
            frame_window = frame_window[1:n_sequence]

            count = 0

            if text_show[0] == "2":
                count = count + 1
            else:
                count = 0
            
            if count == 1:
                cv2.putText(frame, 'Warning!!!', (300,50), font, 0.8, (0, 0, 225), 2, cv2.LINE_AA)
                actionlist.append(text_show[0])           

            cv2.imshow('Action Recognition', frame)
            if time.time() - start > 10:
                start = time.time()
                namevideo = str(datetime.datetime.now())              
                video_file = os.path.join('output', namevideo + ".avi")
                video_writer = cv2.VideoWriter(
                    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
                )
                print("Send record to vps...")
                send_vps()
                for dirpath, dirnames,filenames in os.walk('/home/anthai/Desktop/real-time-action-recognition/output/'):
                    recordlist.extend(filenames)
                    break               
                if len(recordlist) >= 2:
                    if os.path.exists(os.path.join('output',str(recordlist[0]))):
                        os.remove(os.path.join('output', str(recordlist[0])))
                        while recordlist:
                            recordlist.pop(0)

                    else:
                        print("The file does not exist") 
                    

            video_writer.write(frame)

                
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        mode = 0
        if mode == 1:
            if actionlist.count('2') == 10:
                print('Finding some one...')
                jpg_name = str(datetime.datetime.now())+ ".jpg"
                path = "/home/anthai/Desktop/real-time-action-recognition/image_alert"
                cv2.imwrite(os.path.join(path , jpg_name), frame)
                alert = "Phát hiện ai đó đang..."
                image_path = "/home/anthai/Desktop/real-time-action-recognition/image_alert"+jpg_name
                print("Sending email...")
                send_email("Cảnh báo!!!",alert,image_path,"thaitruonganlxag91@gmail.com")                
                print("Sending telegram...")
                send_telegram_message('Cảnh báo!!! '+ alert)
                send_telegram_photo(image_path)    

            if actionlist.count('2') == 50:
                actionlist.clear()

    else: 
        break
 
cap.release()

