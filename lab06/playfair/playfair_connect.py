import sys
import requests
from PyQt5 import QtWidgets

# Đảm bảo import đúng đường dẫn file UI của bạn (như bạn đã sửa thành công ở bước trước)
from ui.playfair import Ui_MainWindow 

# Đây là địa chỉ API Flask mà bạn đã tạo ở file api.py
API_URL = "http://127.0.0.1:5000/api/playfair"

class PlayfairApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Cài đặt font chữ cho ô Ma Trận để nó dóng hàng thẳng tắp cho đẹp
        self.ui.txt_Ge.setStyleSheet("font-family: Consolas, Courier New; font-size: 14pt;")

        # --- LIÊN KẾT NÚT BẤM VỚI HÀM ---
        self.ui.btn_Ge.clicked.connect(self.generate_matrix)
        self.ui.btn_En.clicked.connect(self.encrypt_text)
        self.ui.btn_De.clicked.connect(self.decrypt_text)

    # 1. HÀM TẠO MA TRẬN
    def generate_matrix(self):
        key = self.ui.txt_K.toPlainText().strip()
        if not key:
            self.ui.txt_Ge.setText("⚠️ Vui lòng nhập Key trước!")
            return

        try:
            # Gửi Key xuống API /creatematrix
            response = requests.post(f"{API_URL}/creatematrix", json={"key": key})
            data = response.json()
            
            matrix = data.get("playfair_matrix", [])
            
            # Trình bày mảng 5x5 thành chuỗi vuông vức để in ra UI
            display_text = ""
            for row in matrix:
                display_text += "  ".join(row) + "\n"
                
            self.ui.txt_Ge.setText(display_text)
        except Exception as e:
            self.ui.txt_Ge.setText(f"Lỗi kết nối Server!\nBạn đã chạy file api.py chưa?\nChi tiết: {e}")

    # 2. HÀM MÃ HÓA
    def encrypt_text(self):
        plain_text = self.ui.txt_Pl.toPlainText().strip()
        key = self.ui.txt_K.toPlainText().strip()
        
        if not plain_text or not key:
            self.ui.txt_Cip.setText("⚠️ Vui lòng nhập đủ PlainText và Key!")
            return

        try:
            # Gửi xuống API /encrypt
            payload = {"plain_text": plain_text, "key": key}
            response = requests.post(f"{API_URL}/encrypt", json=payload)
            data = response.json()
            
            # In kết quả ra ô Cipher Text
            self.ui.txt_Cip.setText(data.get("encrypted_text", "Không có dữ liệu"))
        except Exception as e:
            self.ui.txt_Cip.setText(f"Lỗi: {e}")

    # 3. HÀM GIẢI MÃ
    def decrypt_text(self):
        cipher_text = self.ui.txt_Cip.toPlainText().strip()
        key = self.ui.txt_K.toPlainText().strip()
        
        if not cipher_text or not key:
            self.ui.txt_Pl.setText("⚠️ Vui lòng nhập đủ Cipher Text và Key!")
            return

        try:
            # Gửi xuống API /decrypt
            payload = {"cipher_text": cipher_text, "key": key}
            response = requests.post(f"{API_URL}/decrypt", json=payload)
            data = response.json()
            
            # In kết quả giải mã ra ô PlainText
            self.ui.txt_Pl.setText(data.get("decrypted_text", "Không có dữ liệu"))
        except Exception as e:
            self.ui.txt_Pl.setText(f"Lỗi: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())