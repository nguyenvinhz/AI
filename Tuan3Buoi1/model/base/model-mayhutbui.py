import random

state = [[random.randint(0,1) for _ in range(4)] for _ in range(4)]

visited = set()

def P_moves(x, y):
    moves = []
    if y < 3:
        moves.append("RIGHT")
    if x < 3:
        moves.append("DOWN")
    if y > 0:
        moves.append("LEFT")
    if x > 0:
        moves.append("UP")
    return moves

def print_state(x, y):
    for i in range(4):
        for j in range(4):
            if (i, j) == (x, y):
                print("P", end=" ")
            else:
                print(state[i][j], end=" ")
        print()

def choose_move(x, y):
    visited.add((x, y))
    priority = ["RIGHT", "DOWN", "LEFT", "UP"]
    for move in priority:
        if move in P_moves(x, y):
            nx, ny = x, y
            if move == "UP":
                nx -= 1
            elif move == "DOWN":
                nx += 1
            elif move == "LEFT":
                ny -= 1
            elif move == "RIGHT":
                ny += 1
            if (nx, ny) not in visited:
                return move
    return None

def main():
    step = 0
    x = random.randint(0, 3)
    y = random.randint(0, 3)

    while True:
        print_state(x, y)

        if state[x][y] == 1:
            print(f"Máy hút bụi đã hút bụi tại vị trí ({x}, {y})")
            state[x][y] = 0

        if all(state[i][j] == 0 for i in range(4) for j in range(4)):
            print("Xong gòi")
            break

        moves = P_moves(x, y)
        print(f"Có thể di chuyển tiếp theo đến: {moves}")

        move = choose_move(x, y)

        if move is None:
            print("Không còn đường mới để đi")
            break

        print(f"Máy hút bụi di chuyển tiếp theo: {move}")

        if move == "UP":
            x -= 1
        elif move == "DOWN":
            x += 1
        elif move == "LEFT":
            y -= 1
        elif move == "RIGHT":
            y += 1

        print()

if "__main__" == __name__:
    main()