from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Label
from textual.screen import Screen
from textual import events

EMPTY_SYMBOL = ' '
X_SYMBOL = 'X'
O_SYMBOL = 'O'


class TicTacToe(App):
    CSS_PATH = "./style.tcss"

    def compose(self) -> ComposeResult:
        for _ in range(3):
            yield GameColumn()

    def get_symbols_grid(self) -> list[list[str]]:
        symbols = []

        for column in self.query_children(GameColumn):
            row = []
            for field in column.query_children(Field):
                row.append(field.current_symbol)
            symbols.append(row)
        return symbols

    def check_row(self, row):
        symbol = row[0]
        if symbol == EMPTY_SYMBOL:
            return None

        for symbols in row:
            if symbol != symbols:
                return None
            return symbol

    def check_column(self, grid:list[list[str]], column_index: int):
        symbol = grid[0][column_index]
        if symbol == EMPTY_SYMBOL:
            return None
        
        for i in range(3):
            if symbol != grid[i][column_index]:
                return None
        return symbol

    def check_first_slope(self, grid:list[list[str]]):
        symbol = grid[0][0]
        if symbol == EMPTY_SYMBOL:
            return None

        for i in range(1, 2):
            if symbol != grid[i][i]:
                return None
        return symbol

    def check_second_slope(self, grid:list[list[str]]):
        symbol = grid[2][0]
        if symbol == EMPTY_SYMBOL:
            return None

        if symbol != grid[1][1] or symbol != grid[0][2]:
            return None

        return symbol

    def check_slopes(self, grid: list[list[str]]):
        self.check_first_slope(grid)


    def get_winning_symbol(self):
        grid = self.get_symbols_grid()


class GameColumn(Horizontal):
    def compose(self) -> ComposeResult:
        for _ in range(3):
            yield Field()

class Field(Label):
    def __init__(self) -> None:
        self.current_symbol = X_SYMBOL
        super().__init__(self.current_symbol, classes="game-field")

    def set_new_symbol(self, symbol):
        self.symbol = symbol

def run():
    app = TicTacToe()
    app.run()
