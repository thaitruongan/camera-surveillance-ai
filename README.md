# HỆ THỐNG CAMERA GIÁM SÁT THÔNG MINH PHỤC VỤ CHĂM SÓC SỨC KHỎE TẠI NHÀ 
Đề tài này là hệ thống nhận dạng hành động thông qua video thời gian thực, phục vụ giám sát cảnh báo khi xảy ra các hành động nguy hiểm gây ảnh hưởng đến sức khỏe. Tôi sử dụng dataset KARD và thêm vào 1 số hành động nguy hiểm tự thu thập để huấn luyện mô hình nhận dạng.
![alt text](https://https://github.com/thaitruongan/camera-surveillance-ai/blob/master/media/output.gif "demo")
## Các thư viện yêu cầu
*	Keras
*	Tensorflow
*	OpenCV
*	Môi trường Anaconda Python
*	Ubuntu 20.04 (một số thư viện có thể khó cài đặt trên hệ điều hành window)
## Dataset
Tải xuống dataset từ đường dẫn này
https://data.mendeley.com/datasets/k28dtm7tr6/1
Skeleton joints và Depth data không được sử dụng trong bài này. Chỉ sử dụng phần video RGB. Để chuẩn bị dataset để huấn luyện, cần tạo cấu trúc folder chưa các video như bên dưới.
```
Dataset
├── a01                   
│   ├── a01_s01_e01.mp4             
│   ├── a01_s01_e02.mp4            
│   ├── ...           
│   ├── a01_s10_e03     
├── a02                   
│   ├── a02_s01_e01.mp4             
│   ├── a02_s01_e02.mp4            
│   ├── ...           
│   ├── a02_s10_e03      
├── ....
├── ....
├── a18                   
│   ├── a18_s01_e01.mp4             
│   ├── a18_s01_e02.mp4            
│   ├── ...           
│   ├── a18_s10_e03   
└── ...
```
Có thể xem thêm chi tiết trong thư mục dataset_list/trainlist.txt và dataset_list/testlist.txt



# Hướng dẫn chạy chương trình

Trước khi chạy chương trình theo hướng dẫn, nên lưu ý đổi lại các đường dẫn để tránh lỗi sai đường dẫn và cài đặt đầy đủ các thư viện cần thiết.

## Demo

Yêu cầu sử dụng Webcam hoặc bất kỳ camera để làm nguồn thu cho video thời gian thực. Chạy lệnh sau để chạy demo
```
python camera.py
```
```
python3 camera.py
```

## Đánh giá mô hình

Để xem độ chính xác và ma trận nhầm lẫn của mô hình sau khi huấn luyện, chạy lệnh sau để đánh giá mô hình
```
python evaluate_model.py
```
```
python3 evaluate_model.py
```

## Huấn luyện mô hình

Để huấn luyện mô hình, chạy lệnh sau để tiến hành huấn luyện mô hình
```
python train.py
```
```
python3 train.py
```
Để thay đổi các tham số, vào file train.py. Các tham số thay đổi cần lưu ý:
Các tham số mặc định không nên thay đổi:
* dim = (224,224) độ dài, độ rộng của khung hình MobileNetV2.
* n_sequence = 8 LSTM
* n_channels = 3 kênh màu RGB

Các tham số có thể thay đổi:
* n_output: số lớp hành động học
* batch_size: số lượng mẫu dữ liệu trong một batch
* n_mul_train: số lượng dữ liệu được gia tăng cho huấn luyện
* n_mul_test: số lượng dữ liệu được gia tăng cho đánh giá
* path_dataset: đường dẫn đến thư mục chứa các video dataset đã chuẩn bị.

## Hiệu suất

Độ chính xác: 90 – 94% (ngẫu nhiên dựa trên tập dữ liệu thử nghiệm).

Confusion Matrix: 
![alt text](https://github.com/peachman05/action-recognition-tutorial/blob/master/media/confusion_matrix.png "Confusion Matrix")

## Phương pháp sử dụng
 
Input: 8 khung hình RGB

Output: lớp hành động

* Đề tài chỉ sử dụng duy nhất một mô hình đơn giản để giải quyết bài toán. Tôi chỉ sử dụng LSTM là phần cốt lõi của mô hình và sử dụng mạng MobileNetV2 để rút trích đặc trưng, lấy ý tưởng từ bài báo [paper](https://arxiv.org/abs/1705.02953) và [project](https://github.com/AhmedGamal1496/online-action-recognition#Introduction). Có thể xem thêm kiến trúc mô hình trong file model_ML.py
* Khi thử nghiệm và đánh giá, tôi sẽ lấy ngẫu nhiên n_sequence khung hình từ mỗi tệp video. Vì vậy n_sequence khung hình là “1 mẫu”. Trong khi thử nghiệm nếu chúng ta chỉ lấy ngẫu nhiên 1 mẫu trên 1 tệp video là không tốt vì độ chính xác sẽ không ổn định. Vì vậy, chúng ta cần lấy ngẫu nhiên nhiều mẫu hơn cho mỗi tệp. Ví dụ: trong eval_model.py, tôi đặt 'n_mul_test' thành 2. Có nghĩa là tôi sẽ chọn ngẫu nhiên 2 mẫu cho mỗi tệp video. Bạn có thể thay đổi n_mul_test thành bất kỳ giá trị nào. Nếu giá trị cao, độ chính xác sẽ ổn định nhưng cần thêm thời gian thử nghiệm.

## Ghi chú

* Các tham số của train.py, eval_model.py và webcam.py nằm trong phần đầu của tệp. Có thể điều chỉnh nó.

* Nếu gặp phải vấn đề hết bộ nhớ khi cố gắng đánh giá hoặc huấn luyện, có thể giảm n_batch và n_sequence để giảm mức tiêu thụ bộ nhớ. Tôi đề nghị không nên sử dụng n_batch = 1 vì độ chính xác sẽ rất lung lay và không thể hội tụ.

## Lời cảm ơn
#### An Giang University(AGU)
Giảng viên hướng dẫn: Dr. Doan Thanh Nghi

## Tham Khảo
### Example code
[https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly](https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly) Data generator on keras  
[https://github.com/eriklindernoren/Action-Recognition](https://github.com/eriklindernoren/Action-Recognition) Sampling Idea  
[https://github.com/AhmedGamal1496/online-action-recognition#Introduction](https://github.com/AhmedGamal1496/online-action-recognition#Introduction) RGB Difference Example
### Bài báo
Temporal Segment Networks for Action Recognition in Videos, Limin Wang, Yuanjun Xiong, Zhe Wang, Yu Qiao, Dahua Lin, Xiaoou Tang, and Luc Van Gool, TPAMI, 2018. [Arxiv Preprint](https://arxiv.org/abs/1705.02953)
### Dataset
[https://data.mendeley.com/datasets/k28dtm7tr6/1](https://data.mendeley.com/datasets/k28dtm7tr6/1)
