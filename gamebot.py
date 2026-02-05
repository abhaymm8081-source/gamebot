from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8016672930:AAE9oeDbf08ISz85ubvNMhea89nkKBpzt0Q"

questions = [
    {"q":"भारत की राजधानी क्या है?", "options":["Delhi","Mumbai","Chennai","Kolkata"], "ans":"Delhi"},
    {"q":"2+5 कितना होता है?", "options":["5","7","9","10"], "ans":"7"},
    {"q":"Sun किस दिशा से निकलता है?", "options":["North","East","West","South"], "ans":"East"}
]

index = 0
score = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global index, score
    index = 0
    score = 0
    await send_question(update.message.chat_id, context)

async def send_question(chat_id, context):
    global index
    if index >= len(questions):
        await context.bot.send_message(chat_id,f"🏆 Game Over! Score = {score}")
        return
    
    q = questions[index]
    buttons = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]]
    reply = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(chat_id,q["q"],reply_markup=reply)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global index, score
    query = update.callback_query
    await query.answer()

    if query.data == questions[index]["ans"]:
        score += 1
        await query.edit_message_text("✅ Sahi jawab!")
    else:
        await query.edit_message_text(f"❌ Galat! sahi tha {questions[index]['ans']}")

    index += 1
    await send_question(query.message.chat_id, context)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
