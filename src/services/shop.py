ITEMS = [
    {'id': 'small_potion', 'name': 'Малое зелье', 'price': 15, 'effect': {'hp': 20}},
    {'id': 'energy_drink', 'name': 'Энергетик', 'price': 20, 'effect': {'energy': 3}},
    {'id': 'iron_sword', 'name': 'Железный меч', 'price': 80, 'effect': {'attack': 3}},
    {'id': 'leather_armor', 'name': 'Кожаный доспех', 'price': 70, 'effect': {'defense': 2}},
]

def shop_event(player):
    text = 'Магазин предметов:\n'
    for item in ITEMS:
        text += f"- {item['name']} — {item['price']} золота.\n"
    text += '\nПокупка предметов пока не реализована, это демо-версия.'
    return text, player
