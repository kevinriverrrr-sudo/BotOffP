export function createNewPlayer(telegramUser) {
  return {
    id: String(telegramUser.id),
    name: telegramUser.first_name || 'Герой',
    level: 1,
    exp: 0,
    nextLevelExp: 100,
    gold: 50,
    hp: 100,
    maxHp: 100,
    energy: 10,
    maxEnergy: 10,
    attack: 5,
    defense: 2,
    wins: 0,
    loses: 0,
    inventory: [],
    lastAdventureAt: 0,
  };
}

let memoryStore = new Map();

export async function loadPlayer(userId, telegramUser) {
  if (memoryStore.has(userId)) {
    return memoryStore.get(userId);
  }
  const player = createNewPlayer(telegramUser);
  memoryStore.set(userId, player);
  return player;
}

export async function savePlayer(userId, player) {
  memoryStore.set(userId, player);
}
