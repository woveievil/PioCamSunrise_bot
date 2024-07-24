import cv2
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
    await update.message.reply_text('Привет! Нажмите /snapshot, чтобы сделать снимок.')

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frame = get_screenshot()
    if frame is None:
        await update.message.reply_text('Не удалось получить снимок.')
        return
    
    _, buffer = cv2.imencode('.jpg', frame)
    io_buf = np.array(buffer).tobytes()

    await context.bot.send_photo(chat_id=update.message.chat_id, photo=io_buf)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("snapshot", snapshot))

    application.run_polling()

if __name__ == '__main__':
    main()
