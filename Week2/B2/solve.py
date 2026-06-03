import copy

table = [
    [1,3,5],
    [4,6,8],
    [2,7,'.']
]

def print_table(s):
    for row in s:
        print(row)
    print()

def find_empty(s):
    for i in range(3):
        for j in range(3):
            if s[i][j] == '.':
                return i,j

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
        "UP":(-1,0),
        "DOWN":(1,0),
        "LEFT":(0,-1),
        "RIGHT":(0,1)
    }
    dx, dy = moves[action]
    new_x = x + dx
    new_y = y + dy
    new_table = copy.deepcopy(s)
    new_table[x][y], new_table[new_x][new_y] = new_table[new_x][new_y], new_table[x][y]
    return new_table

def rule_math(state, rules):
    for rule in rules:
        new_table = execute_action(state, rule)
        print(rule)
        print_table(new_table)

def main():
    print("Trạng thái ban đầu: ")
    print_table(table)
    RULES = find_action(table)
    rule_math(table, RULES)

if  __name__ == "__main__":
    main()