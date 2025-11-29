MEMORY = {}

def create_new_player(tg_user):
    return {
        'id': tg_user.id,
        'name': tg_user.first_name or 'Герой',
        'level': 1,
        'exp': 0,
        'next_level_exp': 100,
        'gold': 50,
        'hp': 100,
        'max_hp': 100,
        'energy': 10,
        'max_energy': 10,
        'attack': 5,
        'defense': 2,
        'wins': 0,
        'loses': 0,
        'inventory': [],
        'last_adventure_at': 0,
    }

async def get_player(tg_user):
    uid = tg_user.id
    if uid in MEMORY:
        return MEMORY[uid]
    player = create_new_player(tg_user)
    MEMORY[uid] = player
    return player

async def save_player(uid, player):
    MEMORY[uid] = player
