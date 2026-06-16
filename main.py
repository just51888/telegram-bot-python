# -*- coding: utf-8 -*-
import os
import urllib.parse
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7709655209  # 你的管理员 ID

name_map = {
    "songbai": "94松白会所部长",
    "honghua": "94红花会所部长",
    "minsheng": "94民生会所部长",
    "huafa": "94华发会所部长",
    "tianyuan": "94田园会所部长",
    "tianliao": "94田寮会所部长",
    "jinyuwan": "94金御湾会所部长",
    "kangle": "95-96康乐会所部长",
    "gongming": "光明链接",
    "jinyu": "金鱼",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_code = context.args[0] if context.args else None
    user_id = update.effective_user.id
    username = update.effective_user.username or "无用户名"

    if raw_code:
        try:
            code = urllib.parse.unquote(raw_code)
        except:
            code = raw_code
    else:
        code = None

    if code and code in name_map:
        chinese = name_map[code]
        print(f"用户 {user_id} ({username}) 通过 {code}（{chinese}）进入")
        await update.message.reply_text(f"兄弟 已经转接：{chinese}")
        if ADMIN_ID:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 新用户来源：\n用户ID: {user_id}\n用户名: @{username}\n来源: {chinese}")
    elif code:
        print(f"用户 {user_id} ({username}) 通过中文链接 {code} 进入")
        await update.message.reply_text(f"兄弟 已经转接：{code}")
        if ADMIN_ID:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 新用户来源：\n用户ID: {user_id}\n用户名: @{username}\n来源: {code}")
    else:
        print(f"用户 {user_id} ({username}) 直接开始")
        await update.message.reply_text("欢迎！")

async def getlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("用法：/getlink 中文名称\n例如：/getlink 微信")
        return
    chinese = " ".join(context.args)
    encoded = urllib.parse.quote(chinese)
    link = f"https://t.me/{context.bot.username}?start={encoded}"
    await update.message.reply_text(f"新链接（平台会显示中文）：\n{link}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getlink", getlink))
    print("机器人已启动，按 Ctrl+C 停止")
    app.run_polling()

if __name__ == "__main__":
    main()
