class Line():
    """
    Creates a list with N amount of \u25a1.
    on init it has an optional to set the amount of blocks,
    defaults to 3 blocks created if no arg is given.

    also contains func for creating the row header as well as a
    func for checking the values in an entire row,
    """
    def __init__(self, nmbr=3):
        self.i = 0
        self.lines = []
        while self.i < nmbr:
            self.lines.append("\u25a1")
            self.i += 1

    def create_row_header(self, nmbr=3):
        """
        Creates the row header to be printed at the bottom.
        Arg is nmbr of rows to make a header for.
        """
        self.number = 0
        self.i = 0
        while self.i < len(self.lines):
            self.lines[self.i] = str(self.number)
            self.number += 1
            self.i += 1

    def check_row(self):
        """
        Checks the values in the rows.
        Returns False if first value is default value
        or if any value is not the same as the inital
        value
        """
        self.comparison = self.lines[0]
        for val in self.lines:
            if self.comparison == "\u25a1":
                return False
            elif self.comparison != val:
                return False
        return True


class Board():
    """
    Board is a class containing a lists filled with instances
    of the class Line. It is essentially a 2d-list.
    takes nmbr of rows and creates a matrix with that heigh and width.
    Defaults to 3x3 game grid.
    """
    def __init__(self, nmbr_of_rows=3):
        self.row_matrix = []
        self.row_length = nmbr_of_rows
        self.line_length = nmbr_of_rows
        self.i = 0
        self.row = Line(self.line_length)
        self.row.create_row_header(self.row_length)
        self.turn = 0
        self.nmbr_to_win = nmbr_of_rows
        self.valid_moves_made = []
        while self.i < self.row_length:
            self.row_matrix.append(Line(self.line_length))
            self.i += 1

    def display_board(self):
        self.i = self.row_length
        for x in reversed(self.row_matrix):
            print(f'{self.i-1}:{x.lines}')
            self.i -= 1
        print(f'\u25e4 {self.row.lines}')

    def legal_move(self, coordinates):
        """
        Checks if coordinate x,y is free and if it is inside
        the board limits.
        Converts the coordinates to a list while splitting on ','.
        Takes the first argument and the final argument as x and y.
        Prints errors based on illegal moves and returns False.
        Returns True if values are not occupied and inside board limits
        """
        try:
            coordinates = list(coordinates.split(','))
            x = int(coordinates[0])
            y = int(coordinates[-1])
            if len(coordinates) < 2:
                print('Endast en valid koordinat angiven!')
                return False
            if self.row_matrix[y].lines[x] != "\u25a1":
                print(f'{x}, {y} är upptaget: {self.row_matrix[y].lines[x]}')
                return False
            else:
                return True
        except AttributeError as c:
            print(c)
        except IndexError as e:
            print(f'{e} \ndu är utanför koordinatsystemet!')
        except ValueError as b:
            print(f'{b} \nAnvänd siffror.')

    def move_piece(self, coordinates, marker):
        """
        Moves pieces. Needs argument for what to input
        on the coordinates. Takes first and last result of the list
        passed as coordinates. Does no error checking, so use
        the legal_move function to check for legality.
        """
        coordinates = list(coordinates.split(','))
        x = int(coordinates[0])
        y = int(coordinates[-1])
        self.row_matrix[y].lines[x] = marker
        self.valid_moves_made.append([x, y])

    def save_end_of_game(self, winner):
        """
        Appends to a file called tic_tac_toe_data.txt
        Writes all of the valid moves made followed by an argument
        passed to the function.
        """
        try:
            with open('tic_tac_toe_data.txt', 'a') as f:
                f.write(f'{str(self.valid_moves_made)}, ')
                f.write(f'{str(winner)}, {str(self.row_length)}')
                f.write("\n")
                print('Spelet sparades')
        except Exception as e:
            print(e)

    def load_replay(self, in_progress=True):
        """
        Defaults to only return games in progress.
        Takes all of the games of the right size that are
        saved as in-progress/finished and puts them into a 2d list.
        [y][n] for game y with n number of moves.
        Final value of the final [y][n] is a bool determining
        how the next helper function will act.
        Returns the entire 2d list to be proccessed.
        """
        self.format_moves = []
        self.y = 0
        if in_progress:
            val = 'InPr\n'
        else:
            val = ['Diag', 'Vert', 'Hori', 'Draw']
        try:
            with open('tic_tac_toe_data.txt', 'r') as t:
                while True:
                    self.n = 0
                    self.x = 1
                    self.raw_moves = []
                    self.line = t.readline()
                    if not self.line:
                        break
                    self.checker = self.line.split(', ')
                    if self.checker[-1][:-1] != str(self.line_length):
                        continue
                    if self.checker[-2] in val:
                        for self.char in self.line[:-8]:
                            try:
                                self.char = int(self.char)
                                self.raw_moves.append(self.char)
                            except Exception:
                                pass
                        self.format_moves.append([])
                        while True:
                            try:
                                self.cord = str(self.raw_moves[self.n])
                                self.coord = str(self.raw_moves[self.x])
                                self.cooord = self.cord + ", " + self.coord
                                self.format_moves[self.y].append([self.cooord])
                                self.n += 2
                                self.x += 2
                            except Exception:
                                self.y += 1
                                break
                        else:
                            continue
        except FileNotFoundError as e:
            print(e)
            menu_loop()
        return self.format_moves, in_progress

    def save_game(self):
        try:
            with open('tic_tac_toe_data.txt', 'a') as f:
                f.write(f'{str(self.valid_moves_made)}, InPr, ')
                f.write(f'{str(self.row_length)}')
                f.write("\n")
                print('Save successful!')
        except Exception as e:
            print(e)
            print('Kunde inte spara, vet ej varför!')
            menu_loop()

    def print_stats(self, matrix=3):
        self.nmbr_wins_circle = 0
        self.nmbr_wins_cross = 0
        self.total_games = 0
        self.avrg_moves = 0
        self.avrg_moves_circle = 0
        self.avrg_moves_cross = 0
        self.matrix = matrix
        self.nmbr_win_how = {'Diag': 0, 'Hori': 0, 'Vert': 0, 'Draw': 0}
        try:
            with open('tic_tac_toe_data.txt', 'r') as f:
                while True:
                    self.line = f.readline()
                    if not self.line:
                        break
                    self.old_moves = self.line[2:-12].split('], [')
                    self.old_winners = self.line.split(', ')
                    if self.old_winners[-1][:-1] != str(self.matrix):
                        continue
                    if self.old_winners[-2] == 'InPr':
                        continue
                    if self.old_winners[-2] == 'Draw':
                        self.nmbr_win_how['Draw'] += 1
                        self.total_games += 1
                        self.avrg_moves += len(self.old_moves)
                        continue
                    if len(self.old_moves) % 2 == 0:
                        self.nmbr_wins_cross += 1
                        self.avrg_moves_cross += len(self.old_moves)
                        self.avrg_moves += len(self.old_moves)
                    elif len(self.old_moves) % 2 == 1:
                        self.nmbr_wins_circle += 1
                        self.avrg_moves_circle += len(self.old_moves)
                        self.avrg_moves += len(self.old_moves)
                    self.total_games += 1
                    self.nmbr_win_how[self.old_winners[-2]] += 1
        except Exception as e:
            print(e)
        self.avrg_moves = self.avrg_moves / self.total_games
        print(
             f'Notera enbart statistik för {self.matrix}*{self.matrix}!\n'
             f'\u25ce vinster: {self.nmbr_wins_circle}\n'
             f'\u2716 totala vinster: {self.nmbr_wins_cross}\n'
             f'Totalt spelade spel: {self.total_games}\n'
             f'Vinster beroende på typ av vinst:\n{self.nmbr_win_how}\n'
             f'Drag i snitt för vinst: {self.avrg_moves}'
        )

    def list_comparison(self, values):
        self.comparison = values[0]
        for self.val in values:
            if self.comparison == "\u25a1":
                return False
            elif self.comparison != self.val:
                return False
        return True

    def win_condition(self):
        if self.turn == (self.line_length * self.row_length):
            print("Brädet är fullt!")
            self.save_end_of_game('Draw')
            return True
        for n in range(0, self.row_length):
            if (
                self.row_matrix[n].check_row()
            ):
                print(f'{self.row_matrix[n].lines[0]} vinner horisontellt!')
                self.save_end_of_game('Hori')
                return True
        for n in range(0, self.line_length):
            self.lister = []
            for y in range(0, self.line_length):
                self.lister.append(self.row_matrix[y].lines[n])
                if len(self.lister) == self.line_length:
                    if self.list_comparison(self.lister):
                        print(f'{self.lister[0]} vinner lodrätt!')
                        self.save_end_of_game('Vert')
                        return True
                    else:
                        self.lister = []
        self.lister = []
        for n in range(0, self.line_length):
            self.lister.append(self.row_matrix[n].lines[n])
            if len(self.lister) == self.line_length:
                if self.list_comparison(self.lister):
                    print(f'{self.row_matrix[0].lines[0]} vinner diagonalt!')
                    self.save_end_of_game('Diag')
                    return True
        self.lister = []
        for n in range(0, self.line_length):
            self.fix = self.line_length - n - 1
            self.lister.append(self.row_matrix[n].lines[self.fix])
            if len(self.lister) == self.line_length:
                if self.list_comparison(self.lister):
                    self.t = self.row_matrix[self.line_length-1].lines[0]
                    print(f'{self.t} vinner diagonalt!')
                    self.save_end_of_game('Diag')
                    return True

    def next_move(self):
        if self.turn % 2 == 0:
            self.val = "\u25ce"
        else:
            self.val = "\u2716"
        self.move = input(f"Skriv in koordinater för {self.val}: ")
        if self.move == 'Save':
            self.save_game()
            menu_loop()
        exit_test(self.move)
        self.move = ','.join(self.move.split())
        if self.legal_move(self.move):
            self.move_piece(self.move, self.val)
            self.turn += 1
            self.display_board()
            return self.win_condition()
        else:
            return self.win_condition()
            self.next_move()

    def select_loaded_game(self, loaded_list):
        """
        Helper function to the load_replay func.
        Takes the 2d-list from load_replay and asks the user
        which replay to replay.
        If replays were loaded, it goes back into the main game-loop.
        If a complete file was loaded, goes back to the menu.
        """
        self.load_list = loaded_list[0]
        self.load_inprogress = loaded_list[-1]
        print(f'Du har {len(self.load_list)} sparade spel')
        self.choice = input(
            f'Välj ett sparat spel från 1 till {len(self.load_list)}: '
            )
        exit_test(self.choice)
        try:
            self.choice = int(self.choice)-1
            self.load_list[self.choice]
        except TypeError:
            print("Felaktig inmatning. Försök igen.")
            self.select_loaded_game(loaded_list)
        except IndexError:
            print('Finns inget här!')
            menu_loop()
        self.turn = 0
        for i in self.load_list[self.choice]:
            self.s = str(i)
            self.send = str(self.s[2]) + ', ' + str(self.s[5])
            if self.turn % 2 == 0:
                self.move_piece(self.send, "\u25ce")
            else:
                self.move_piece(self.send, "\u2716")
            print(f'Drag nummer {self.turn+1}:')
            self.display_board()
            print('')
            self.turn += 1
        if self.load_inprogress:
            self.game_loop()
        else:
            self.win = 'nobody'
            if self.turn % 2 == 0:
                self.win = '\u2716'
            else:
                self.win = '\u25ce'
            print(f'{self.win} vann efter {self.turn} drag.')

    def game_loop(self):
        self.game_complete = False
        while self.game_complete is not True:
            self.game_complete = self.next_move()


print('''
Skriv Exit för att avsluta programmet.
Skriv Save för att spara ett pågående spel.
''')


def exit_test(arg):
    """
    Checks if input was 'Exit' and terminates
    program if it was
    """
    if arg == 'Exit':
        quit(0)


def menu_loop():
    selection = input(
                     'Vill du:\n'
                     'Påbörja nytt spel: 1\n'
                     'Ladda spelat/pågående spel: 2\n'
                     'Visa statistik: 3\n'
        )
    exit_test(selection)
    if (selection.lower()).strip() == "2":
        choice = False
        while choice is False:
            select = input(
                          'Ladda ett avslutat spel: 1\n'
                          'Ladda ett pågående spel: 2\n'
                          )
            exit_test(select)
            if select not in ['1', '2']:
                print('1 eller 2!')
                continue
            sizer = input(
                          'Storlek på ena dimensionen på matrisen'
                          ' att söka.\nDvs input*input matris'
                          '(felaktig input defaultar till "3"'
                          ', dvs söker efter 3x3 matris)\n'
                          )
            exit_test(sizer)
            try:
                sizer = int(sizer)
            except Exception:
                sizer = 3
                print('Defaultar till 3x3\n')
            if select == '1':
                choice = True
                game_board = Board(sizer)
                game_board.select_loaded_game(game_board.load_replay(False))
            elif select == '2':
                choice = True
                game_board = Board(sizer)
                game_board.select_loaded_game(game_board.load_replay(True))
            else:
                print('Försök igen')
    elif selection.strip() == '1':
        size = input(
            'Storlek på spelbrädet?\n'
            '3 ger 3x3, 5 ger 5x5 osv.\n'
            'Defaultar till 3x3 om dålig input!\n'
            )
        exit_test(size)
        try:
            size = int(size)
        except Exception:
            print('Går ej att konvertera till int - defaultar till 3x3-bräde!')
            size = 3
        game_board = Board(size)
        game_board.display_board()
        game_board.game_loop()
    elif selection.strip() == '3':
        size = input('Vilken storlek på brädet vill du ha statistik från?')
        exit_test(size)
        try:
            size = int(size)
        except Exception:
            print('Default till 3x3')
            size = 3
        game_board = Board(size)
        try:
            game_board.print_stats(size)
        except ZeroDivisionError:
            print('Inga spel sparade med den storleken!')

    menu_loop()


menu_loop()
