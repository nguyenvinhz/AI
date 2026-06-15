import copy

table = [
    [1,3,5],
    [4,'.',8],
    [2,7,6]
]

goal = [
    [1,2,3],
    [4,5,6],
    [7,8,'.']
]

def print_table(s):
    for row in s:
        print(row)
    print()

def find_empty(s):
    for i in range(3):
        for j in range(3):
            if s[i][j] == '.':
                return i, j

def rule_match(s):
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
        "UP": (-1,0),
        "DOWN": (1,0),
        "LEFT": (0,-1),
        "RIGHT": (0,1)
    }
    dx, dy = moves[action]
    nx = x + dx
    ny = y + dy
    new_table = copy.deepcopy(s)
    new_table[x][y], new_table[nx][ny] = new_table[nx][ny], new_table[x][y]
    return new_table

def score_solve(s):
    score = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] == goal[i][j]:
                score += 1
    return score

def simple_reflex(state):
    while state != goal:
        print_table(state)
        rules = rule_match(state)
        best_score = -1
        best_state = None
        for action in rules:
            new_state = execute_action(state, action)
            score = score_solve(new_state)
            if score > best_score:
                best_score = score
                best_state = new_state
        state = best_state
    print_table(state)

def main():
    simple_reflex(table)

if __name__ == "__main__":
    main()