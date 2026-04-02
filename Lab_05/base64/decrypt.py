import base64

def main():
    try:
        # Mở và đọc nội dung từ tệp data.txt
        with open("data.txt", "r") as file:
            encoded_string = file.read().strip()

        # Giải mã chuỗi Base64
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")

        print("Chuỗi sau khi giải mã:", decoded_string)
        
    except Exception as e:
        print("Lỗi:", e)

if __name__ == "__main__":
    main()
    