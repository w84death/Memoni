import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import random
import time

class MemoryGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Game")

        self.num_players = 2  # Number of players
        self.num_pairs = 12  # Number of pairs of cards
        self.deck = self.create_deck(self.num_pairs)
        self.current_player = 0
        self.scores = [0] * self.num_players
        self.selected_cards = []
        self.buttons = {}
        self.cards_flipped = set()
        self.disable_buttons = False

        self.player_turn_label = tk.Label(self.master, text=f"Player {self.current_player + 1}'s turn")
        self.player_turn_label.grid(row=0, column=0, columnspan=5)

        self.setup_board()

    def setup_board(self):
        for index in self.buttons:
            self.buttons[index].destroy()
        self.buttons.clear()
        for index, (card_id, pair_id) in enumerate(self.deck):
            button = tk.Button(self.master, text="?", command=lambda idx=index: self.reveal_card(idx), height=2, width=5)
            button.grid(row=(index // 5) + 1, column=index % 5)
            self.buttons[index] = button
        self.default_color = self.buttons[0].cget('background')

    def create_deck(self, num_pairs):
        deck = [(card_id, pair_id) for pair_id in range(1, num_pairs + 1) for card_id in (1, 2)]
        random.shuffle(deck)
        return deck

    def reveal_card(self, index):
        if index in self.cards_flipped or self.disable_buttons or len(self.selected_cards) == 2:
            return  # Card is already flipped or clicks are disabled

        card_id, pair_id = self.deck[index]
        self.buttons[index].config(text=str(pair_id), bg='lightblue')  # Change background color when card is revealed
        self.selected_cards.append((index, pair_id))

        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
        idx1, pair_id1 = self.selected_cards[0]
        idx2, pair_id2 = self.selected_cards[1]

        if pair_id1 == pair_id2:
            self.scores[self.current_player] += 1
            self.cards_flipped.update({idx1, idx2})
            self.selected_cards = []
            self.disable_buttons = False
            if self.check_game_over():
                self.end_game()
        else:
            self.master.after(1000, self.hide_cards)
            self.disable_buttons = True

    def hide_cards(self):
        for index, pair_id in self.selected_cards:
            if index not in self.cards_flipped:
                self.buttons[index].config(text="?", bg=self.default_color)
        self.selected_cards = []
        self.disable_buttons = False
        self.current_player = (self.current_player + 1) % self.num_players
        self.player_turn_label.config(text=f"Player {self.current_player + 1}'s turn")

    def check_game_over(self):
        # Corrected the check condition here
        return len(self.cards_flipped) == 2 * self.num_pairs

    def end_game(self):
        for index in self.buttons:
            self.buttons[index].config(state="disabled", bg=self.default_color)

        result_window = tk.Toplevel(self.master)
        result_window.title("Results")
        result_text = "Game Over!\n\n"
        for i, score in enumerate(self.scores):
            result_text += f"Player {i + 1} scored {score} points.\n"
        result_label = tk.Label(result_window, text=result_text, padx=20, pady=20)
        result_label.pack(side="top")

        ok_button = tk.Button(result_window, text="OK", command=lambda: [result_window.destroy(), self.reset_game()])
        ok_button.pack(side="bottom", pady=10)

    def reset_game(self):
        self.deck = self.create_deck(self.num_pairs)
        self.current_player = 0
        self.scores = [0] * self.num_players
        self.selected_cards = []
        self.cards_flipped = set()
        self.disable_buttons = False
        self.setup_board()
        self.update_turn_label()

    def update_turn_label(self):
        self.player_turn_label.config(text=f"Player {self.current_player + 1}'s turn")


    def show_splash(self, duration=2000):
        # Tworzenie okna splash screen
        splash_root = tk.Toplevel()
        splash_root.overrideredirect(True)  # Usuwa ramkę okna

        # Ustawienie obrazka
        image = Image.open("splash_image.png")  # Upewnij się, że plik istnieje
        self.photo_image = ImageTk.PhotoImage(image)  # Utrzymaj referencję
        splash_label = tk.Label(splash_root, image=self.photo_image)
        splash_label.pack()

        # Centrowanie okna splash screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        splash_root.geometry(f'+{(screen_width - image.width) // 2}+{(screen_height - image.height) // 2}')

        # Zamykanie okna splash screen po określonym czasie i uruchamianie głównej gry
        self.master.after(duration, lambda: [splash_root.destroy(), self.master.deiconify()])

# Uruchomienie głównego okna gry
root = tk.Tk()
root.withdraw()  # Początkowo ukrywa główne okno
game_gui = MemoryGameGUI(root)
game_gui.show_splash(2000)  # Wyświetl splash screen na 2 sekundy
root.mainloop()

