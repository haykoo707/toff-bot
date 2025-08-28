from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

BOT_TOKEN = "8387057499:AAEcmiETPpQ_sRcppJ00peQnwrKIfy-ZAXU"  # քո Telegram Bot-ի Token-ը
REWARD_FILE = "rewards.txt"   # այստեղ կպահվի օգտատերերի reward-ները

@app.route("/reward", methods=["POST"])
def reward():
    data = request.json  # AdsGram-ից եկած json
    if not data:
        return {"status": "error", "message": "No JSON received"}, 400

    user_id = str(data.get("user_id"))
    reward_id = str(data.get("reward_id"))

    # Գրենք txt ֆայլի մեջ
    with open(REWARD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_id} | reward: {reward_id}\n")

    # Ուղարկենք հաղորդագրություն user-ին
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": user_id,
                "text": "Դու ստացար +10 coins 🚀 շնորհակալություն գովազդ դիտելու համար։"
            }
        )
    except Exception as e:
        print("Telegram sendMessage error:", e)

    print(f"✅ User {user_id} finished ad {reward_id}")
    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render-ի համար
    app.run(host="0.0.0.0", port=port)
