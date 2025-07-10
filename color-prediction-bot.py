

import telebot
from collections import Counter, deque
import random

API_TOKEN = '7600921671:AAFdkcuHQ5XLt95vnXu_0jJLHO4S5D3G7CU'
bot = telebot.TeleBot(API_TOKEN)
history = {}

nums_unicode = ['⓪','①','②','③','④','⑤','⑥','⑦','⑧','⑨']
def to_unicode(n): return nums_unicode[n]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, (
        "🎯 *Color Prediction Bot* 🎯\n\n"
        "Send me last 10 numbers like:\n"
        "`/predict 6 8 9 5 8 0 3 1 5 8`\n\n"
        "_Receive AI‑prediction, trend insights, modulo logic._"
    ), parse_mode="Markdown")

@bot.message_handler(commands=['predict'])
def predict(message):
    try:
        parts = message.text.strip().split()
        nums = list(map(int, parts[1:]))
        if len(nums) != 10:
            raise ValueError

        # Track history
        uid = message.from_user.id
        history.setdefault(uid, deque(maxlen=50)).extend(nums)

        freq = Counter(nums)
        hot = [n for n, _ in freq.most_common(2)]
        cold = [n for n in range(10) if n not in freq][:2]

        ai = [n for n, _ in freq.most_common()]
        while len(ai) < 3:
            x = random.randint(0,9)
            if x not in ai: ai.append(x)
        ai = ai[:3]

        mod_groups = {0:[],1:[],2:[]}
        for n in nums:
            mod_groups[n%3].append(n)
        active = max(mod_groups, key=lambda g: len(mod_groups[g]))

        reasons = []
        for x in ai:
            r = []
            if x in hot: r.append("High frequency")
            if x in mod_groups[active]: r.append(f"in Group {active}")
            if x in cold: r.append("Gap filler")
            reasons.append(" + ".join(r) or "Pattern filler")

        response = f"""
🎯 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗜𝗢𝗡 𝗥𝗘𝗣𝗢𝗥𝗧 🔍

🧠 AI MODE:
┣ 💡 Level 1 ➤ {to_unicode(ai[0])} ({reasons[0]})
┣ 💡 Level 2 ➤ {to_unicode(ai[1])} ({reasons[1]})
┗ 💡 Level 3 ➤ {to_unicode(ai[2])} ({reasons[2]})

📊 TREND ANALYSIS:
┣ 🔥 Hot: {', '.join(to_unicode(n) for n in hot)}
┣ 🧊 Cold: {', '.join(to_unicode(n) for n in cold)}
┗ 📈 Max freq: {to_unicode(hot[0])} (x{freq[hot[0]]})

♻️ MODULO GROUPS (mod 3):
┣ 0 ➤ {', '.join(to_unicode(n) for n in mod_groups[0]) or '—'}
┣ 1 ➤ {', '.join(to_unicode(n) for n in mod_groups[1]) or '—'}
┣ 2 ➤ {', '.join(to_unicode(n) for n in mod_groups[2]) or '—'}
┗ ⚡ Most active: Group {active} ✅

📘 LOGIC SUMMARY:
✔ {to_unicode(ai[0])} repeated {freq[ai[0]]} times → Trend
✔ {to_unicode(ai[1])} aligns group {active}
✔ {to_unicode(ai[2])} balances pattern

🔚 Possible winners: {to_unicode(ai[0])} / {to_unicode(ai[1])} / {to_unicode(ai[2])}
"""
        bot.reply_to(message, response.strip(), parse_mode="Markdown")

    except:
        bot.reply_to(message, "❌ Invalid input! Send exactly 10 numbers after /predict.", parse_mode="Markdown")

bot.infinity_polling()
