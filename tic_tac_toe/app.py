from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, Button
from textual.screen import Screen
from typing import cast

EMPTY_SYMBOL = ' '
X_SYMBOL = 'X'
O_SYMBOL = 'O'

class TicTacToe(App):
    CSS_PATH = "./style.tcss"

    BINDINGS = [
            ("q", "quit", "Exit the game")
            ]

    def __init__(self):
        super().__init__()
        self.current_player = X_SYMBOL

    def compose(self) -> ComposeResult:
        yield CurrentSymbolScreen(classes="global-symbol")
        for _ in range(3):
            yield GameColumn()

    def _get_symbols_grid(self) -> list[list[str]]:
        symbols = []

        for column in self.query_children(GameColumn):
            row = []
            for field in column.query_children(Field):
                row.append(field.current_symbol)
            symbols.append(row)
        return symbols

    def _check_row(self, row) -> str | None:
        symbol = row[0]
        if symbol == EMPTY_SYMBOL:
            return None

        for symbols in row:
            if symbol != symbols:
                return None
        return symbol

    def _check_column(self, grid:list[list[str]], column_index: int) -> str | None:
        symbol = grid[0][column_index]
        if symbol == EMPTY_SYMBOL:
            return None
        
        for i in range(3):
            if symbol != grid[i][column_index]:
                return None
        return symbol

    def _check_first_slope(self, grid:list[list[str]]) -> str | None:
        symbol = grid[0][0]
        if symbol == EMPTY_SYMBOL:
            return None

        for i in range(1, 3):
            if symbol != grid[i][i]:
                return None
        return symbol

    def _check_second_slope(self, grid:list[list[str]]) -> str | None:
        symbol = grid[2][0]
        if symbol == EMPTY_SYMBOL:
            return None

        if symbol != grid[1][1] or symbol != grid[0][2]:
            return None

        return symbol

    def _check_slopes(self, grid: list[list[str]]) -> str | None:
        winner = self._check_first_slope(grid)
        if winner is not None:
            return winner
        return self._check_second_slope(grid)

    def check_tie(self) -> bool:
        grid = self._get_symbols_grid()
        for row in grid:
            if EMPTY_SYMBOL in row:
                return False
        return True

    def get_winning_symbol(self) -> str | None:
        grid = self._get_symbols_grid()
        
        for row in grid:
            winner = self._check_row(row)
            if winner is not None:
                return winner

        for i in range(3):
            winner = self._check_column(grid, i)
            if winner is not None:
                return winner

        winner = self._check_slopes(grid)
        if winner is not None:
            return winner

        return None
    
    def handle_game_over(self, button_label: str | None) -> None:
        if button_label == "yes":
            self.current_player = X_SYMBOL
            self.query_one(CurrentSymbolScreen).update_symbol(self.current_player)

            for field in self.query(Field):
                field.current_symbol = EMPTY_SYMBOL
                field.remove_class("player-x", "player-o")
                field.update(EMPTY_SYMBOL)
        else:
            self.exit()

class GameColumn(Horizontal):
    def compose(self) -> ComposeResult:
        for _ in range(3):
            yield Field()

class Field(Label):
    def __init__(self) -> None:
        self.current_symbol = EMPTY_SYMBOL
        super().__init__(self.current_symbol, classes="game-field")

    def set_new_symbol(self, symbol):
        if symbol == EMPTY_SYMBOL:
            return
        self.current_symbol = symbol
        if symbol == X_SYMBOL:
            self.add_class("player-x")
        elif symbol == O_SYMBOL:
            self.add_class("player-o")

        self.update(self.current_symbol)

    def on_click(self):
        if self.current_symbol != EMPTY_SYMBOL:
            return
        my_app = cast(TicTacToe, self.app)

        self.set_new_symbol(my_app.current_player)

        winner = my_app.get_winning_symbol()
        if winner is not None:
            my_app.push_screen(WinnerScreen(winner), my_app.handle_game_over)
            return

        if my_app.check_tie():
            my_app.push_screen(WinnerScreen(None), my_app.handle_game_over)
            return

        if my_app.current_player == X_SYMBOL:
            my_app.current_player = O_SYMBOL
        else:
            my_app.current_player = X_SYMBOL

        self.app.query_one(CurrentSymbolScreen).update_symbol(my_app.current_player)

class CurrentSymbolScreen(Horizontal):
    def compose(self) -> ComposeResult:
        self.symbol_label = Label(X_SYMBOL)
        yield self.symbol_label

    def update_symbol(self, new_symbol: str):
        self.symbol_label.update(f"Aktualny gracz: {new_symbol}")

class WinnerScreen(Screen[str]):
    def __init__(self, winner_symbol) -> None:
        super().__init__()
        self.winner_symbol = winner_symbol

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog-box"):
            if self.winner_symbol is not None:
                yield Label(f"Wygrał gracz: {self.winner_symbol}", classes="dialog-text")
            else:
                yield Label("Remis! Nikt nie wygrał.", classes="dialog-text")

            yield Label("Czy chcesz zagrać ponownie?", classes="dialog-text")

            with Horizontal(classes="dialog-buttons"):
                yield Button("Tak", id="yes", variant="success")
                yield Button("Nie", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)

def run():
    app = TicTacToe()
    app.run()
