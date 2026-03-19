import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect button
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)


    # ================= API CHUNG =================
    def call_api(self, url, method="GET", payload=None):
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=payload, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                QMessageBox.warning(self, "Lỗi", f"API lỗi: {response.status_code}")
                return None

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
            return None


    # ================= GENERATE KEY =================
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"

        data = self.call_api(url)

        if data:
            QMessageBox.information(self, "Thông báo", data.get("message", "Đã tạo key"))


    # ================= ENCRYPT =================
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"

        message = self.ui.txt_plain.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung!")
            return

        payload = {
            "message": message,
            "key_type": "public"
        }

        data = self.call_api(url, "POST", payload)

        if data:
            if "encrypted_message" in data:
                self.ui.txt_cipher.setPlainText(data["encrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã mã hóa dữ liệu!")
            else:
                QMessageBox.warning(self, "Lỗi", data.get("error", "Lỗi mã hóa"))


    # ================= DECRYPT =================
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"

        ciphertext = self.ui.txt_cipher.toPlainText().strip()

        if not ciphertext:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ciphertext!")
            return

        payload = {
            "ciphertext": ciphertext,
            "key_type": "private"
        }

        data = self.call_api(url, "POST", payload)

        if data:
            if "decrypted_message" in data:
                self.ui.txt_plain.setPlainText(data["decrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã giải mã dữ liệu!")
            else:
                QMessageBox.warning(self, "Lỗi", data.get("error", "Lỗi giải mã"))


    # ================= SIGN =================
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"

        message = self.ui.txt_plain_3.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung cần ký!")
            return

        payload = {
            "message": message
        }

        data = self.call_api(url, "POST", payload)

        if data:
            if "signature" in data:
                self.ui.txt_plain_4.setPlainText(data["signature"])
                QMessageBox.information(self, "Thành công", "Đã ký số!")
            else:
                QMessageBox.warning(self, "Lỗi", data.get("error", "Lỗi ký số"))


    # ================= VERIFY =================
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"

        message = self.ui.txt_plain_3.toPlainText().strip()
        signature = self.ui.txt_plain_4.toPlainText().strip()

        if not message or not signature:
            QMessageBox.warning(self, "Lỗi", "Thiếu dữ liệu xác thực!")
            return

        payload = {
            "message": message,
            "signature": signature
        }

        data = self.call_api(url, "POST", payload)

        if data:
            if data.get("is_verified"):
                QMessageBox.information(self, "Xác thực", "Chữ ký HỢP LỆ!")
            else:
                QMessageBox.warning(self, "Xác thực", "Chữ ký KHÔNG đúng!")


# ================= MAIN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())