import cv2
import numpy as np
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# RTSP URL вашей камеры
RTSP_URL = "rtsp://admin:zadvorki666@192.168.0.101/cam/realmonitor?channel=1&subtype=0"

# Токен вашего Telegram-бота
TELEGRAM_TOKEN = '7215985693:AAGwHSOhOJxVB62j_C0f59UaMN1ddHGQ98Y'

def get_screenshot():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    return frame

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Какая погода?", callback_data='snapshot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Нажмите кнопку:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'snapshot':
        frame = get_screenshot()
        if frame is None:
            await query.edit_message_text(text='Не удалось получить снимок.')
            return

        _, buffer = cv2.imencode('.jpg', frame)
        io_buf = np.array(buffer).tobytes()

        await context.bot.send_photo(chat_id=query.message.chat_id, photo=io_buf)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
