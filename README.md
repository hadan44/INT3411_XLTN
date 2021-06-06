# INT3411_XLTN
Đồ án cuối khóa xử lý tiếng nói của Nguyễn Vương Tiến và Nguyễn Sĩ Tùng

- Ở đây với phần nhận diện chúng em sử dụng google api qua thư viện SpeechRecognition để thực hiện nhận diện giọng nói. Trước đây chúng em có quyết định thử mô hình hmm sử dụng thư viện hmmlearn và librosa để train với reference từ:

https://labs.septeni-technology.jp/machine-learning/speech-processing-nhan-dang-giong-noi-bang-mo-hinh-markov-an-hmm/

tuy nhiên tập data của lớp không phù hợp với mục đích của app đặc biệt như từ "tivi" hay từ "đèn" ảnh hưởng tới lệnh điều khiển các thiết bị nên chúng em quyết định đổi sang sử dụng google api

- Chúng em sử dụng thêm thư viện Google Text-to-Speech (gTTS) để thực hiện xác nhận lại những lệnh mà người dùng đưa ra.

- Phần code chính được đặt tại /XLTN/Pi4/sr.p


