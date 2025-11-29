import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from services.player import get_player, save_player
from services.adventure import adventure_event
from services.battle import battle_event
from services.shop import shop_event

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

MAIN_MENU = ReplyKeyboardMarkup([
    ['📜 Профиль', '🚶‍♂️ Приключение'],
    ['⚔️ Бой', '🛒 Магазин']
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = await get_player(user)
    await update.message.reply_text(
        f'Привет, {player["name"]}! Это BotOffP на Python.',
        reply_markup=MAIN_MENU,
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Главное меню:', reply_markup=MAIN_MENU)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = await get_player(user)
    text = (
        f"Имя: {player['name']}\n"
        f"Уровень: {player['level']}\n"
        f"Опыт: {player['exp']}/{player['next_level_exp']}\n"
        f"Золото: {player['gold']}\n"
        f"HP: {player['hp']}/{player['max_hp']}\n"
        f"Энергия: {player['energy']}/{player['max_energy']}\n"
        f"Победы: {player['wins']} | Поражения: {player['loses']}\n"
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU)

async def adventure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = await get_player(user)
    text, updated = adventure_event(player)
    await save_player(user.id, updated)
    await update.message.reply_text(text, reply_markup=MAIN_MENU)

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = await get_player(user)
    text, updated = battle_event(player)
    await save_player(user.id, updated)
    await update.message.reply_text(text, reply_markup=MAIN_MENU)

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player = await get_player(user)
    text, updated = shop_event(player)
    await save_player(user.id, updated)
    await update.message.reply_text(text, reply_markup=MAIN_MENU)

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Жми кнопки меню ниже 🙂', reply_markup=MAIN_MENU)

async def main():
    if not BOT_TOKEN:
        raise RuntimeError('Не указан BOT_TOKEN в .env')

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('menu', menu))
    app.add_handler(MessageHandler(filters.Regex('^📜 Профиль$'), profile))
    app.add_handler(MessageHandler(filters.Regex('^🚶‍♂️ Приключение$'), adventure))
    app.add_handler(MessageHandler(filters.Regex('^⚔️ Бой$'), battle))
    app.add_handler(MessageHandler(filters.Regex('^🛒 Магазин$'), shop))
    app.add_handler(MessageHandler(filters.ALL, fallback))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
