from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токе бота
TOKEN = '6224100382:AAEK9nkW1yt2RXXXB63IilXkpwP2jVaUX9I'

# Словарь для хранения заметок
notes = {}

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Приветик. Я помогу тебе записать все твои дела. /help для подробностей")

# Команда /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать взаимодействие\n"
        "/help - показать это сообщение\n"
        "/create_note <название заметки> <текст заметки> - создать заметку\n"
        "/delete_note <название заметки> - удалить заметку\n"
        "/get_notes - получить список заметок"
    )

# Команда /create_note
def create_note(update: Update, context: CallbackContext) -> None:
    text = context.args
    if len(text) >= 2:
        note_title = text[0]
        note_text = ' '.join(text[1:])
        user_id = update.message.from_user.id
        notes[user_id] = {note_title: note_text}
        update.message.reply_text(f"Заметка '{note_title}' создана.")
    else:
        update.message.reply_text("Используйте /create_note <название заметки> <текст заметки>.")

# Команда /delete_note
def delete_note(update: Update, context: CallbackContext) -> None:
    text = context.args
    if text:
        note_title = text[0]
        user_id = update.message.from_user.id
        if user_id in notes and note_title in notes[user_id]:
            del notes[user_id][note_title]
            update.message.reply_text(f"Заметка '{note_title}' удалена.")
        else:
            update.message.reply_text(f"Заметка с названием '{note_title}' не найдена.")
    else:
        update.message.reply_text("Используйте /delete_note <название заметки>.")

# Команда /get_notes
def get_notes(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in notes and notes[user_id]:
        notes_list = "\n".join([f"{title}: {text}" for title, text in notes[user_id].items()])
        update.message.reply_text(f"Список заметок:\n{notes_list}")
    else:
        update.message.reply_text("Список заметок пуст.")

# Обработка левых сообщений
def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Я понимаю только команды. Используйте /help для списка команд.")

# Создание и запуск бота
def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("create_note", create_note, pass_args=True))
    dp.add_handler(CommandHandler("delete_note", delete_note, pass_args=True))
    dp.add_handler(CommandHandler("get_notes", get_notes))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
