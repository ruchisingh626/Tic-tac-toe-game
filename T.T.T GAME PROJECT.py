import tkinter as tk
from tkinter import messagebox, ttk
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moderate Difficulty Tic Tac Toe")
        self.root.geometry("420x750")
        self.root.resizable(False, False)
        
        # Core States
        self.player_token = "X"
        self.computer_token = "O"
        self.player_name = "Player"
        self.computer_name = "Computer"  
        self.victory_phrase = "You win!"  
        self.is_dark_mode = False  
        
        self.board = [""] * 9
        self.buttons = []
        self.scores = {"player": 0, "computer": 0, "ties": 0}
        
        # Timer variables
        self.time_left = 3
        self.timer_job = None
        
        # Standard Tic Tac Toe grid combinations 
        self.winning_combination = [ [3, 4, 5], [6, 7, 8], [1, 4, 7], [2, 5, 8], [2, 4, 6] ]  # Rows, Columns, Diagonals
    
        
        self.show_setup_screen()

    def show_setup_screen(self):
        """Creates the character choice menu screen."""
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack(pady=60)
        
        lbl_title = tk.Label(self.setup_frame, text="CHOOSE YOUR HERO", font=("arial", 20, "bold"))
        lbl_title.pack(pady=20)
        
        self.characters = {
            "Default (Classic X vs O)": ("X", "O", "Player", "Computer", "You win!"),
            "👸 Queen vs 🐉 Dragon": ("👸", "🐉", "Queen", "Dragon", "Queen wins! Long live the Queen!"),
            "🤵 King vs 🧙‍♂️ Wizard": ("🤵", "🧙‍♂️", "King", "Wizard", "King wins! All hail the King!"),
            "🧑‍🚀 Astronaut vs 👽 Alien": ("🧑‍🚀", "👽", "Astronaut", "Alien", "Astronaut wins! Deep space victory!"),
            "🐱 Cat vs 🐶 Dog": ("🐱", "🐶", "Cat", "Dog", "Cat wins! Meow-velous victory!")
        }
        
        lbl_choose = tk.Label(self.setup_frame, text="Select Profile Theme:", font=("arial", 12))
        lbl_choose.pack(pady=5)
        
        self.char_combo = ttk.Combobox(self.setup_frame, values=list(self.characters.keys()), state="readonly", width=25)
        self.char_combo.current(0)
        self.char_combo.pack(pady=10)
        
        btn_start = tk.Button(self.setup_frame, text="Start Match", font=("arial", 14, "bold"), bg="#4CAF50", fg="white", cursor="hand2", padx=10, command=self.confirm_character)
        btn_start.pack(pady=30)

    def confirm_character(self):
        """Unpacks chosen variables and launches main interface."""
        selected_theme = self.char_combo.get()
        self.player_token, self.computer_token, self.player_name, self.computer_name, self.victory_phrase = self.characters[selected_theme]
        
        self.setup_frame.destroy()
        self.build_game_ui()
        self.start_countdown()

    def build_game_ui(self):
        """Builds game loop arena with theme support."""
        self.theme_frame = tk.Frame(self.root)
        self.theme_frame.pack(anchor="ne", padx=10, pady=5)
        
        self.theme_button = tk.Button(
            self.theme_frame, text="🌙 Dark Mode", font=("arial", 10, "bold"),
            command=self.toggle_theme, bd=1, relief="groove", cursor="hand2"
        )
        self.theme_button.pack()

        self.title_label = tk.Label(self.root, text="TIC TAC TOE", font=("arial", 28, "bold"))
        self.title_label.pack(pady=5) 

        # Timer Countdown UI Label
        self.timer_label = tk.Label(self.root, text="Time Left: 3s", font=("arial", 16, "bold"), fg="#7B1FA2")
        self.timer_label.pack(pady=2)

        self.score_label = tk.Label(self.root, text="", font=("arial", 12, "bold"))
        self.score_label.pack(pady=5)
        self.update_score_display()

        self.status_label = tk.Label(self.root, text=f"Your turn ({self.player_token})", font=("arial", 14))
        self.status_label.pack(pady=10)

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        for i in range(9):
            button = tk.Button(
                self.game_frame, font=("arial", 22, "bold"), width=5, height=2,
                command=lambda i=i: self.player_move(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.buttons.append(button)

        self.apply_theme_colors()

    # ⏱️ TIMER MANAGEMENT
    def start_countdown(self):
        self.stop_countdown()
        self.time_left = 3
        self.update_timer_loop()

    def stop_countdown(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer_loop(self):
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        if self.time_left <= 0:
            self.status_label.config(text="Time out! Skipping turn...")
            self.root.after(500, self.computer_move)
            return
        self.time_left -= 1
        self.timer_job = self.root.after(1000, self.update_timer_loop)

    # 🌗 THEME CONFIGURATION
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme_colors()

    def apply_theme_colors(self):
        if self.is_dark_mode:
            bg_main = "#1E1E1E"       
            bg_card = "#2D2D2D"       
            fg_main = "#FFFFFF"       
            btn_bg = "#3A3A3A"        
            btn_text = "#E0E0E0"      
            toggle_text = "☀️ Light Mode"
            timer_fg = "#E1BEE7"
        else:
            bg_main = "#FFFFFF"       
            bg_card = "#F5F5F5"       
            fg_main = "#000000"       
            btn_bg = "#EAEAEA"        
            btn_text = "#000000"      
            toggle_text = "🌙 Dark Mode"
            timer_fg = "#7B1FA2"

        self.root.config(bg=bg_main)
        self.theme_frame.config(bg=bg_main)
        self.game_frame.config(bg=bg_main)
        
        self.title_label.config(bg=bg_main, fg=fg_main)
        self.status_label.config(bg=bg_main, fg=fg_main)
        self.timer_label.config(bg=bg_main, fg=timer_fg)
        self.score_label.config(bg=bg_main, fg="#9FA8DA" if self.is_dark_mode else "#1A237E")
        
        self.theme_button.config(text=toggle_text, bg=btn_bg, fg=fg_main, activebackground=bg_card, activeforeground=fg_main)
        
        for i, btn in enumerate(self.buttons):
            if self.board[i] == "":
                btn.config(bg=btn_bg, fg=btn_text, activebackground=bg_card)
            else:
                btn.config(bg=bg_card)

    def check_winner(self, player):
        for combo in self.winning_combination:
            if all(self.board[pos] == player for pos in combo):
                return combo
        return None

    def is_draw(self):
        return "" not in self.board

    def update_score_display(self):
        self.score_label.config(
            text=f"{self.player_name}: {self.scores['player']}  |  {self.computer_name}: {self.scores['computer']}  |  Ties: {self.scores['ties']}"
        )

    def flash_win(self, combination_indices, count=0):
        if count >= 6:
            return
        current_color = "#4CAF50" if count % 2 == 0 else "#81C784"
        for idx in combination_indices:
            self.buttons[idx].config(bg=current_color, disabledforeground="white")
        self.root.after(250, lambda: self.flash_win(combination_indices, count + 1))

    # 🤝 POST-GAME OPTIONS BOX (CONTINUE OR RESTART)
    def show_end_game_options(self, message_title, message_text):
        choice = messagebox.askyesnocancel(
            message_title, 
            f"{message_text}\n\nClick 'Yes' to CONTINUE (Next Round)\nClick 'No' to RESTART (Clear Scores)\nClick 'Cancel' to Stay"
        )
        if choice is True:    
            self.reset_game()
        elif choice is False: 
            self.total_restart()

    def reset_game(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state='normal')
        self.status_label.config(text=f"Your turn ({self.player_token})")
        self.apply_theme_colors()
        self.start_countdown()

    def total_restart(self):
        self.stop_countdown()
        self.board = [""] * 9
        self.buttons = []
        self.scores = {"player": 0, "computer": 0, "ties": 0}
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.show_setup_screen()

    # 🤖 MODERATE DIFFICULTY LOGIC CHANGER (60% PLAYER WIN RATIO MATH)
    def computer_move(self):
        self.stop_countdown()
        available_moves = [i for i in range(9) if self.board[i] == ""]
        if not available_moves: return

        chosen_move = None

        # Probability Engine: 35% chance to skip smart logic and make a random flaw
        if random.random() < 0.35:
            chosen_move = random.choice(available_moves)
        else:
            # 65% chance to execute perfect block/win scanning patterns
            # 1. Look to win instantly
            for i in available_moves:
                self.board[i] = self.computer_token
                if self.check_winner(self.computer_token):
                    chosen_move = i
                    self.board[i] = ""
                    break
                self.board[i] = ""

            # 2. Look to block player 
            if chosen_move is None:
                for i in available_moves:
                    self.board[i] = self.player_token
                    if self.check_winner(self.player_token):
                        chosen_move = i
                        self.board[i] = ""
                        break
                    self.board[i] = ""

            # 3. Secure center or corners if open
            if chosen_move is None:
                if 4 in available_moves:
                    chosen_move = 4
                else:
                    corners = [c for c in [0, 2, 6, 8] if c in available_moves]
                    if corners:
                        chosen_move = random.choice(corners)

            # 4. Fallback random picker
            if chosen_move is None:
                chosen_move = random.choice(available_moves)

        self.board[chosen_move] = self.computer_token
        fg_marker = "#FF5252" if self.is_dark_mode else "#D32F2F"
        bg_marker = "#2D2D2D" if self.is_dark_mode else "#F5F5F5"
        self.buttons[chosen_move].config(
            text=self.computer_token, 
            state="disabled", 
            bg=bg_marker, 
            disabledforeground=fg_marker
        )
        
        cpu_win_combo = self.check_winner(self.computer_token)
        if cpu_win_combo:
            self.stop_countdown()
            self.disable_board()
            self.scores["computer"] += 1
            self.update_score_display()
            msg = f"{self.computer_name} wins!"
            self.status_label.config(text=msg)
            self.flash_win(cpu_win_combo)
            self.root.after(1500, lambda: self.show_end_game_options("Game Over", msg))
            return
            
        if self.is_draw():
            self.stop_countdown()
            self.disable_board()
            self.scores["ties"] += 1
            self.update_score_display()
            self.status_label.config(text="It is a draw")
            self.root.after(1500, lambda: self.show_end_game_options("Game Over", "It is a draw!"))
            return
            
        self.status_label.config(text=f"Your turn ({self.player_token})")
        self.start_countdown()

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def player_move(self, index):
        if self.board[index] != "": 
            return
        self.stop_countdown()
            
        self.board[index] = self.player_token
        
        fg_marker = "#40C4FF" if self.is_dark_mode else "#1976D2"
        bg_marker = "#2D2D2D" if self.is_dark_mode else "#F5F5F5"
        self.buttons[index].config(
            text=self.player_token, 
            state="disabled", 
            bg=bg_marker, 
            disabledforeground=fg_marker
        )
        
        player_win_combo = self.check_winner(self.player_token)
        if player_win_combo:
            self.stop_countdown()
            self.disable_board()
            self.scores["player"] += 1
            self.update_score_display()
            self.status_label.config(text=self.victory_phrase)
            self.flash_win(player_win_combo)
            self.root.after(1500, lambda: self.show_end_game_options("Victory!", self.victory_phrase))
            return
            
        if self.is_draw():
            self.stop_countdown()
            self.disable_board()
            self.scores["ties"] += 1
            self.update_score_display()
            self.status_label.config(text="It is a draw")
            self.root.after(1500, lambda: self.show_end_game_options("Game Over", "It is a draw!"))
            return
            
        self.status_label.config(text=f"{self.computer_name} thinking...")
        self.root.after(400, self.computer_move)

if __name__ == "__main__":
    window = tk.Tk()
    app = TicTacToeApp(window)
    window.mainloop()

