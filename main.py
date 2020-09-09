import random
import os

def generate_line():
    line = []
    while len(line) < 3:
        choice = random.choice(choices)
        if choice == '🚆' and line.count('🚆') == 2:
            continue
        line.append(choice)
    return line

choices = ['🚆', '💰', '🛤 ']

arr = []

for i in range(15):
    line = generate_line()
    arr.append(line)


arr[-1][1] = '🚶'
os.system('clear')

coins = 0

print(f'Coins: {coins}' )
for i in arr:
    print((' '*10).join(i))

while True:
    user_input = input('\n')
    user_position = arr[-1].index('🚶')
    if user_input.lower() == 'a':
        user_position = 0
    elif user_input.lower() == 's':
        user_position = 1
    elif user_input.lower() == 'd':
        user_position = 2
    arr.pop()
    arr.insert(0, generate_line())
    if arr[-1][user_position] == '💰':
        coins +=1 
    elif arr[-1][user_position] == '🚆':
        os.system('clear')
        print(f'Earned coins: {coins}')
        break
    arr[-1][user_position] = '🚶'
    os.system('clear')
    print(f'Coins: {coins}' )
    for i in arr:
        print((' '*10).join(i))
