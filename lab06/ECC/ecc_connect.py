import sys
import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from ui.ecc_ui import Ui_MainWindow

API_URL = "http://127.0.0.1:5000/api/ecc"

class ECCApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_ge.clicked.connect(self.generate_keys)
        self.ui.btn_sig.clicked.connect(self.sign_message)
        self.ui.btn_ver.clicked.connect(self.verify_signature)

    def generate_keys(self):
        try:
            response = requests.get(f"{API_URL}/generate_keys")
            data = response.json()
            
            QMessageBox.information(self, "Thành công", data.get("message", "Đã tạo Key thành công!"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi API", f"Lỗi kết nối Server! Bạn đã bật api.py chưa?\nChi tiết: {e}")

    def sign_message(self):
        message = self.ui.txt_infor.toPlainText().strip()
        
        if not message:
            QMessageBox.warning(self, "Cảnh báo", "⚠️ Vui lòng nhập Information (Thông điệp) cần ký!")
            return

        try:
            # Gửi dữ liệu xuống API /sign
            payload = {"message": message}
            response = requests.post(f"{API_URL}/sign", json=payload)
            data = response.json()
            
            self.ui.txt_sig.setText(data.get("signature", ""))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tạo chữ ký: {e}")

    def verify_signature(self):
        message = self.ui.txt_infor.toPlainText().strip()
        signature = self.ui.txt_sig.toPlainText().strip()
        
        if not message or not signature:
            QMessageBox.warning(self, "Cảnh báo", "⚠️ Vui lòng nhập đủ Information và Signature để xác thực!")
            return

        try:
            payload = {"message": message, "signature": signature}
            response = requests.post(f"{API_URL}/verify", json=payload)
            data = response.json()
            
            is_verified = data.get("is_verified", False)
            
            if is_verified:
                QMessageBox.information(self, "Kết quả Verify", " Chữ ký HỢP LỆ!\nThông điệp này là chính chủ và chưa bị chỉnh sửa.")
            else:
                QMessageBox.warning(self, "Kết quả Verify", " Chữ ký KHÔNG HỢP LỆ!\nThông điệp có thể đã bị giả mạo hoặc chữ ký sai.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xác thực: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())