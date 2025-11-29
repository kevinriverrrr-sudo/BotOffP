import random
import time

def adventure_event(player):
    now = int(time.time())
    cooldown = 20

    if now - player['last_adventure_at'] < cooldown:
        left = cooldown - (now - player['last_adventure_at'])
        return f'Подожди ещё {left} сек. перед следующим приключением.', player

    if player['energy'] <= 0:
        return 'У тебя закончилась энергия. Отдохни немного!', player

    player['energy'] -= 1
    player['last_adventure_at'] = now

    roll = random.random()

    if roll < 0.5:
        gold = random.randint(10, 25)
        player['gold'] += gold
        text = f'Ты нашёл сундук и получил {gold} золота!'
    elif roll < 0.8:
        exp = random.randint(15, 35)
        player['exp'] += exp
        text = f'Ты выполнил мини-квест и получил {exp} опыта!'
    else:
        player['hp'] -= 10
        if player['hp'] < 0:
            player['hp'] = 0
        text = 'Ты попал в ловушку и потерял немного HP!'

    level_up(player)
    return text, player

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
