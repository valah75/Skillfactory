def none2space(a):
    if a is None:
        return " "
    else:
        return a


def welcome():
    strlen = 28
    print("-" * strlen)
    print("Welcome".center(strlen))
    print("to the game".center(strlen))
    print("Tic Tac Toe".center(strlen))
    print("-" * strlen)
    print("format for data input: x y".center(strlen))
    print("x - row number".center(strlen))
    print("y - column number".center(strlen))
    print("-" * strlen)


def showf():  # Show game field
    print()
    print("    | 0 | 1 | 2 | ")
    print("  --------------- ")
    for i, row in enumerate(field):
        row_str = f"  {i} | {' | '.join(map(none2space, row))} | "
        print(row_str)
        print("  --------------- ")
    print()


def ask():
    while True:
        coordinates = input("         Your move: ").split()

        if len(coordinates) == 2:

            x = coordinates[0]
            y = coordinates[1]

            if x.isdigit() and y.isdigit():

                x = int(x)
                y = int(y)

                if (0 <= x <= 2) and (0 <= y <= 2):

                    if field[x][y] is None:

                        return x, y  # Returning function values

                    else:
                        print(" The cell is busy! ")
                        continue

                else:
                    print(" The coordinates are out of range ! ")
                    continue

            else:
                print(" Please enter non-negative numbers! ")
                continue

        else:
            print(" Please enter 2 coordinates! ")
            continue


def check_win():
    win_tuples = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for coord in win_tuples:
        symbols = []
        for c in coord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("X wins!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("0 wins!!!")
            return True
    return False


welcome()

field = [[None] * 3 for i in range(3)]

count = 0

while True:
    count += 1

    # Turn of gamers

    showf()
    if count % 2 == 1:
        print(" Turn of X!")
    else:
        print(" Turn of 0!")

    x, y = ask()

    # Filling the field cell

    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    # Verifying the result of game

    if check_win():
        break

    if count == 9:
        print(" Dead heat!")
        break
