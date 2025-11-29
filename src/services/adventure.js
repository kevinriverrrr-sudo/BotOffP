export function handleAdventure(player) {
  const now = Date.now();
  const cooldown = 20_000; // 20 секунд

  if (now - player.lastAdventureAt < cooldown) {
    const left = Math.ceil((cooldown - (now - player.lastAdventureAt)) / 1000);
    return {
      text: `Подожди ещё ${left} сек. перед следующим приключением.`,
      updatedPlayer: player,
    };
  }

  if (player.energy <= 0) {
    return {
      text: 'У тебя закончилась энергия. Отдохни немного!',
      updatedPlayer: player,
    };
  }

  player.energy -= 1;
  player.lastAdventureAt = now;

  const roll = Math.random();
  let text = '';

  if (roll < 0.5) {
    const gold = 10 + Math.floor(Math.random() * 15);
    player.gold += gold;
    text = `Ты нашёл сундук и получил ${gold} золота!`;
  } else if (roll < 0.8) {
    const exp = 15 + Math.floor(Math.random() * 20);
    player.exp += exp;
    text = `Ты выполнил мини-квест и получил ${exp} опыта!`;
  } else {
    player.hp -= 10;
    if (player.hp < 0) player.hp = 0;
    text = 'Ты попал в ловушку и потерял немного HP!';
  }

  levelUpCheck(player);

  return { text, updatedPlayer: player };
}

export function levelUpCheck(player) {
  while (player.exp >= player.nextLevelExp) {
    player.exp -= player.nextLevelExp;
    player.level += 1;
    player.nextLevelExp = Math.floor(player.nextLevelExp * 1.6);
    player.maxHp += 10;
    player.hp = player.maxHp;
    player.maxEnergy += 1;
    player.energy = player.maxEnergy;
    player.attack += 2;
    player.defense += 1;
  }
}
