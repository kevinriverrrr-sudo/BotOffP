import 'dotenv/config';
import { Telegraf, Markup } from 'telegraf';
import { loadPlayer, savePlayer } from './services/playerStore.js';
import { handleAdventure } from './services/adventure.js';
import { handleBattle } from './services/battle.js';
import { handleShop } from './services/shop.js';

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start(async (ctx) => {
  const userId = String(ctx.from.id);
  const player = await loadPlayer(userId, ctx.from);

  await ctx.reply(
    `Привет, ${player.name}! Это BotOffP — текстовый RPG-бот.`,
    mainMenu()
  );
});

bot.command('menu', async (ctx) => {
  await ctx.reply('Главное меню:', mainMenu());
});

bot.hears('📜 Профиль', async (ctx) => {
  const userId = String(ctx.from.id);
  const player = await loadPlayer(userId, ctx.from);

  const profile = `
Имя: ${player.name}
Уровень: ${player.level}
Опыт: ${player.exp}/${player.nextLevelExp}
Золото: ${player.gold}
HP: ${player.hp}/${player.maxHp}
Энергия: ${player.energy}/${player.maxEnergy}
Победы: ${player.wins} | Поражения: ${player.loses}
`;
  await ctx.reply(profile, mainMenu());
});

bot.hears('🚶‍♂️ Приключение', async (ctx) => {
  const userId = String(ctx.from.id);
  const player = await loadPlayer(userId, ctx.from);

  const { text, updatedPlayer } = handleAdventure(player);
  await savePlayer(userId, updatedPlayer);

  await ctx.reply(text, mainMenu());
});

bot.hears('⚔️ Бой', async (ctx) => {
  const userId = String(ctx.from.id);
  const player = await loadPlayer(userId, ctx.from);

  const { text, updatedPlayer } = handleBattle(player);
  await savePlayer(userId, updatedPlayer);

  await ctx.reply(text, mainMenu());
});

bot.hears('🛒 Магазин', async (ctx) => {
  const userId = String(ctx.from.id);
  const player = await loadPlayer(userId, ctx.from);

  const { text, updatedPlayer } = handleShop(player);
  await savePlayer(userId, updatedPlayer);

  await ctx.reply(text, mainMenu());
});

bot.catch((err, ctx) => {
  console.error('Bot error:', err);
  ctx.reply('Произошла ошибка, попробуй ещё раз позже.');
});

bot.launch().then(() => {
  console.log('BotOffP запущен');
});

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

function mainMenu() {
  return Markup.keyboard([
    ['📜 Профиль', '🚶‍♂️ Приключение'],
    ['⚔️ Бой', '🛒 Магазин'],
  ]).resize();
}
