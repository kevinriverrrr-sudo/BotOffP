export function handleBattle(player) {
  if (player.energy <= 0) {
    return {
      text: 'У тебя нет энергии для боя.',
      updatedPlayer: player,
    };
  }

  player.energy -= 1;

  const enemy = createEnemy(player.level);

  const playerPower = player.attack + Math.random() * 5;
  const enemyPower = enemy.attack + Math.random() * 5;

  let text = '';

  if (playerPower >= enemyPower) {
    const gold = 20 + Math.floor(Math.random() * 20);
    const exp = 25 + Math.floor(Math.random() * 25);
    player.gold += gold;
    player.exp += exp;
    player.wins += 1;
    text = `Победа над ${enemy.name}! Ты получил ${gold} золота и ${exp} опыта.`;
  } else {
    const hpLoss = 15 + Math.floor(Math.random() * 15);
    player.hp -= hpLoss;
    if (player.hp < 0) player.hp = 0;
    player.loses += 1;
    text = `Поражение от ${enemy.name}. Ты потерял ${hpLoss} HP.`;
  }

  levelUpCheck(player);

  return { text, updatedPlayer: player };
}

function createEnemy(level) {
  const names = ['Гоблин', 'Разбойник', 'Скелет', 'Дикий зверь', 'Огр'];
  return {
    name: names[Math.floor(Math.random() * names.length)],
    attack: 3 + level * 2,
    defense: 1 + level,
    hp: 30 + level * 10,
  };
}

function levelUpCheck(player) {
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
