from flask import Flask, request
import requests
import os

app = Flask(__name__)
BOT_TOKEN = os.environ.get("8387057499:AAEcmiETPpQ_sRcppJ00peQnwrKIfy-ZAXU")
REWARD_FILE = "rewards.txt"

@app.route("/reward", methods=["POST"])
def reward():
    # AdsGram ուղարկում է query param userId
    user_id = request.args.get("userId")  # <-- սա [userId]-ից կստանա իրական ID
    reward_id = request.json.get("reward_id") if request.json else "unknown"

    # Գրենք txt ֆայլի մեջ
    with open(REWARD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_id} | reward: {reward_id}\n")

    # Telegram հաղորդագրություն
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": user_id,
                "text": "Դու ստացար +10 coins 🚀"
            }
        )
    except Exception as e:
        print("Telegram sendMessage error:", e)

    print(f"✅ User {user_id} finished ad {reward_id}")
    return {"status": "ok"}, 200
