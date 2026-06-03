import random

state = [[random.randint(0,1) for _ in range(4)] for _ in range(4)]

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

def main():
    step = 0
    x, y = random.randint(0, 3), random.randint(0, 3)
    print(f"Máy hút bụi bắt đầu tại vị trí ({x}, {y})")
    
    while True:
        print_state(x, y)
        if state[x][y] == 1:
            print(f"Máy hút bụi đã hút bụi tại vị trí ({x}, {y})")
            state[x][y] = 0

        moves = P_moves(x, y)
        print(f"Có thể di chuyển tiếp theo đến: {moves}")
        move = random.choice(moves) 
        print(f"Máy hút bụi di chuyển tiếp theo: {move}")
        if move == "UP":
            x -= 1
        elif move == "DOWN":
            x += 1
        elif move == "LEFT":
            y -= 1
        elif move == "RIGHT":
            y += 1
        step += 1
        
        if all(state[i][j] == 0 for i in range(4) for j in range(4)):
            print("Xong gòi")
            break
        
        print()

    print(step)

if "__main__" == __name__:
    main()