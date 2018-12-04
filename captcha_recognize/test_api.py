import requests
url = "http://127.0.0.1:6000/b"
files = {'image_file': ('5949_captcha69.jpg', open('/home/linhanqiu/Proj/cnn_captcha/sample/test/5949_captcha69.jpg', 'rb'), 'application')}
r = requests.post(url=url, files=files)
print(r.json())