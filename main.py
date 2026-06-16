# -*- coding: utf-8 -*-
import os
import urllib.parse
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

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

    # 1. 先尝试 URL 解码（将编码的中文还原）
    decoded_code = None
    if raw_code:
        try:
            decoded_code = urllib.parse.unquote(raw_code)
        except:
            decoded_code = raw_code

    # 2. 如果解码后的参数在 name_map 中（拼音链接），用映射的中文回复
    if decoded_code and decoded_code in name_map:
        chinese = name_map[decoded_code]
        print(f"用户 {user_id} 通过拼音 {decoded_code}（{chinese}）进入")
        await update.message.reply_text(f"兄弟 已经转接：{chinese}")
    # 3. 如果解码后的参数不在 name_map 中，但本身是中文（中文链接），直接使用
    elif decoded_code:
        print(f"用户 {user_id} 通过中文链接 {decoded_code} 进入")
        await update.message.reply_text(f"兄弟 已经转接：{decoded_code}")
    else:
        print(f"用户 {user_id} 直接开始")
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
