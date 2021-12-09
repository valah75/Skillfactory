from random import randint

class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "You're trying to shoot outside the board!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "You have already shot to this cell!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    """
    Parameters of the Ship:

    lenght - length of the Ship.
    bow - the point where the bow of the Ship is located.
    orientation - the direction of the Ship (vertical/horizontal).
    lives - the number of lives (how many points of the Ship have not been hit yet).

    """
    def __init__(self, bow, l, o):
        self.bow = bow
        self.length = l
        self.orientation = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i

            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots



class Board:
    """
    Описание класса Board:
        Двумерный список, в котором хранятся состояния каждой из клеток.
        Список кораблей доски.
        Параметр hidden типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет
        (для своей доски).
        Количество живых кораблей на доске.

    И имеет методы:

        1. add_ship - который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
        2. contour - который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке
            кораблей (помечает соседние точки, где корабля по правилам быть не может).
        3. str - который выводит доску в консоль в зависимости от параметра hidden.
        4. out - который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля,
            и False, если не выходит.
        5. shot - который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку,
            нужно выбрасывать исключения).

    """
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hidden = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hidden:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("The ship is destroyed!")
                    return False
                else:
                    print("The ship is damaged!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Missed!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Turn of Computer: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("   Your move: ").split()

            if len(cords) != 2:
                print(" Please enter 2 coordinates! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Please input numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hidden = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        strlen = 27
        print("-" * strlen)
        print("Welcome".center(strlen))
        print("to the game".center(strlen))
        print("Sea Battle".center(strlen))
        print("-" * strlen)
        print("format for data input: x y".center(strlen))
        print("x - row number".center(strlen))
        print("y - column number".center(strlen))
        print("-" * strlen)

    def loop(self):
        num = 0
        while True:
            strlen = 27
            print("-" * strlen)
            print("User board:")
            print(self.us.board)
            print("-" * strlen)
            print("Computer board:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * strlen)
                print("Turn of User!")
                repeat = self.us.move()
            else:
                print("-" * strlen)
                print("Turn of Computer!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * strlen)
                print("User wins!!!")
                break

            if self.us.board.count == 7:
                print("-" * strlen)
                print("Computer wins!!!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()