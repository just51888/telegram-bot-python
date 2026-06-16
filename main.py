import urllib.parse

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_code = context.args[0] if context.args else None
    user_id = update.effective_user.id

    # 1. URL 解码（将 %E6%B5%8B... 转为中文）
    if raw_code:
        try:
            code = urllib.parse.unquote(raw_code)
        except:
            code = raw_code
    else:
        code = None

    # 2. 如果解码后的参数在 name_map 中（拼音），用映射的中文回复
    if code and code in name_map:
        chinese = name_map[code]
        print(f"用户 {user_id} 通过拼音 {code}（{chinese}）进入")
        await update.message.reply_text(f"兄弟 已经转接：{chinese}")
    # 3. 如果解码后的参数不在 name_map 中，直接使用（支持中文链接）
    elif code:
        print(f"用户 {user_id} 通过中文链接 {code} 进入")
        await update.message.reply_text(f"兄弟 已经转接：{code}")
    else:
        print(f"用户 {user_id} 直接开始")
        await update.message.reply_text("欢迎！")
