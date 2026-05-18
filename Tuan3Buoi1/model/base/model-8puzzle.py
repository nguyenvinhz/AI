import copy
import random

visited = set()

def random_table():
    numbers = list(range(9))
    random.shuffle(numbers)

    table = [numbers[i:i+3] for i in range(0, 9, 3)]

    for i in range(3):
        for j in range(3):
            if table[i][j] == 0:
                table[i][j] = '.'

    return table

def print_table(s):
    for row in s:
        print(row)
    print()

def state_to_string(s):
    return ''.join(str(x) for row in s for x in row)

def find_empty(s):
    for i in range(3):
        for j in range(3):
            if s[i][j] == '.':
                return i, j

def find_action(s):
    x, y = find_empty(s)

    rules = []

    if x > 0:
        rules.append("UP")

    if x < 2:
        rules.append("DOWN")

    if y > 0:
        rules.append("LEFT")

    if y < 2:
        rules.append("RIGHT")

    return rules

def execute_action(s, action):
    x, y = find_empty(s)

    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    dx, dy = moves[action]

    new_x = x + dx
    new_y = y + dy

    new_table = copy.deepcopy(s)

    new_table[x][y], new_table[new_x][new_y] = new_table[new_x][new_y], new_table[x][y]

    return new_table

def choose_action(s):
    visited.add(state_to_string(s))

    priority = ["RIGHT", "DOWN", "LEFT", "UP"]

    for move in priority:
        if move in find_action(s):

            new_state = execute_action(s, move)

            if state_to_string(new_state) not in visited:
                return move

    return None

def solve(start):
    current_state = start

    while True:
        print_table(current_state)

        RULES = find_action(current_state)
        print("Các hướng có thể đi:", RULES)

        move = choose_action(current_state)

        if move is None:
            print("Không có lời giải")
            break

        print("Di chuyển:", move)

        current_state = execute_action(current_state, move)

        print()

def main():
    table = random_table()

    print("Trạng thái ban đầu:")
    print_table(table)

    solve(table)

if __name__ == "__main__":
    main()