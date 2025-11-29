import random

def battle_event(player):
    if player['energy'] <= 0:
        return 'У тебя нет энергии для боя.', player

    player['energy'] -= 1
    enemy = create_enemy(player['level'])

    player_power = player['attack'] + random.uniform(0, 5)
    enemy_power = enemy['attack'] + random.uniform(0, 5)

    if player_power >= enemy_power:
        gold = random.randint(20, 40)
        exp = random.randint(25, 50)
        player['gold'] += gold
        player['exp'] += exp
        player['wins'] += 1
        text = f'Победа над {enemy["name"]}! Ты получил {gold} золота и {exp} опыта.'
    else:
        hp_loss = random.randint(15, 30)
        player['hp'] -= hp_loss
        if player['hp'] < 0:
            player['hp'] = 0
        player['loses'] += 1
        text = f'Поражение от {enemy["name"]}. Ты потерял {hp_loss} HP.'

    level_up(player)
    return text, player

def create_enemy(level):
    names = ['Гоблин', 'Разбойник', 'Скелет', 'Дикий зверь', 'Огр']
    return {
        'name': random.choice(names),
        'attack': 3 + level * 2,
        'defense': 1 + level,
        'hp': 30 + level * 10,
    }

def level_up(player):
    while player['exp'] >= player['next_level_exp']:
        player['exp'] -= player['next_level_exp']
        player['level'] += 1
        player['next_level_exp'] = int(player['next_level_exp'] * 1.6)
        player['max_hp'] += 10
        player['hp'] = player['max_hp']
        player['max_energy'] += 1
        player['energy'] = player['max_energy']
        player['attack'] += 2
        player['defense'] += 1
