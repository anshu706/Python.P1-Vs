import random
import tkinter as tk


class RockPaperScissorsApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Rock Paper Scissors - Neon Arena")
        self.root.geometry("920x620")
        self.root.minsize(860, 580)

        self.palette = {
            "bg": "#0E1320",
            "panel": "#161E32",
            "panel_soft": "#1E2945",
            "accent": "#31E3B6",
            "accent_soft": "#1AA589",
            "danger": "#FF6B7D",
            "warning": "#F9C74F",
            "text": "#EEF4FF",
            "muted": "#9DB0CF",
        }

        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.round_number = 0
        self.options = ["rock", "paper", "scissors"]
        self.choice_buttons: list[tk.Button] = []
        self.glow_job: str | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        self.root.configure(bg=self.palette["bg"])

        bg_canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bg=self.palette["bg"],
            relief="flat",
        )
        bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_canvas.create_oval(-150, -220, 360, 280, fill="#1E3A5F", outline="")
        bg_canvas.create_oval(550, -200, 1060, 320, fill="#173058", outline="")
        bg_canvas.create_oval(260, 360, 900, 980, fill="#142742", outline="")

        main = tk.Frame(self.root, bg=self.palette["bg"])
        main.place(relx=0.5, rely=0.5, anchor="center",
                   relwidth=0.92, relheight=0.9)

        header = tk.Frame(main, bg=self.palette["bg"])
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="NEON ARENA",
            font=("Bahnschrift", 28, "bold"),
            fg=self.palette["text"],
            bg=self.palette["bg"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Rock. Paper. Scissors. Pick your move and challenge the machine.",
            font=("Segoe UI", 11),
            fg=self.palette["muted"],
            bg=self.palette["bg"],
        ).pack(anchor="w", pady=(4, 0))

        self.round_badge = tk.Label(
            header,
            text="ROUND 00",
            font=("Consolas", 10, "bold"),
            fg=self.palette["accent"],
            bg=self.palette["bg"],
        )
        self.round_badge.pack(anchor="e")

        score_row = tk.Frame(main, bg=self.palette["bg"])
        score_row.pack(fill="x", pady=(0, 16))

        self.player_score_value = self._score_card(
            score_row, "PLAYER", "0", self.palette["accent"])
        self.computer_score_value = self._score_card(
            score_row, "COMPUTER", "0", self.palette["danger"])
        self.tie_score_value = self._score_card(
            score_row, "TIES", "0", self.palette["warning"])

        content = tk.Frame(main, bg=self.palette["bg"])
        content.pack(fill="both", expand=True)

        left_panel = tk.Frame(
            content, bg=self.palette["panel"], padx=20, pady=20)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            left_panel,
            text="Choose Your Move",
            font=("Segoe UI", 16, "bold"),
            fg=self.palette["text"],
            bg=self.palette["panel"],
        ).pack(anchor="w")

        tk.Label(
            left_panel,
            text="Each round is instant. First to dominate the board wins the vibe.",
            font=("Segoe UI", 10),
            fg=self.palette["muted"],
            bg=self.palette["panel"],
            wraplength=460,
            justify="left",
        ).pack(anchor="w", pady=(6, 18))

        button_row = tk.Frame(left_panel, bg=self.palette["panel"])
        button_row.pack(fill="x", pady=(0, 20))

        self._choice_button(button_row, "ROCK", "rock", "#2B395E").pack(
            side="left", expand=True, fill="x", padx=(0, 8)
        )
        self._choice_button(button_row, "PAPER", "paper", "#274861").pack(
            side="left", expand=True, fill="x", padx=4
        )
        self._choice_button(button_row, "SCISSORS", "scissors", "#4E2D56").pack(
            side="left", expand=True, fill="x", padx=(8, 0)
        )

        self.result_text = tk.StringVar(value="Make your first move.")
        self.round_text = tk.StringVar(value="Your move: -     Computer: -")

        result_box = tk.Frame(
            left_panel, bg=self.palette["panel_soft"], padx=16, pady=14)
        result_box.pack(fill="x")

        self.result_label = tk.Label(
            result_box,
            textvariable=self.result_text,
            font=("Segoe UI", 14, "bold"),
            fg=self.palette["text"],
            bg=self.palette["panel_soft"],
        )
        self.result_label.pack(anchor="w")

        self.result_box = result_box

        tk.Label(
            result_box,
            textvariable=self.round_text,
            font=("Segoe UI", 10),
            fg=self.palette["muted"],
            bg=self.palette["panel_soft"],
        ).pack(anchor="w", pady=(4, 0))

        action_row = tk.Frame(left_panel, bg=self.palette["panel"])
        action_row.pack(fill="x", pady=(20, 0))

        tk.Button(
            action_row,
            text="Reset Scores",
            font=("Segoe UI", 10, "bold"),
            bg="#233455",
            fg=self.palette["text"],
            activebackground="#2F426A",
            activeforeground=self.palette["text"],
            bd=0,
            padx=16,
            pady=10,
            command=self.reset_scores,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            action_row,
            text="Quit",
            font=("Segoe UI", 10, "bold"),
            bg="#3E2435",
            fg=self.palette["text"],
            activebackground="#5A304A",
            activeforeground=self.palette["text"],
            bd=0,
            padx=20,
            pady=10,
            command=self.root.destroy,
            cursor="hand2",
        ).pack(side="right")

        right_panel = tk.Frame(
            content, bg=self.palette["panel"], padx=20, pady=20)
        right_panel.pack(side="right", fill="y", padx=(10, 0))

        tk.Label(
            right_panel,
            text="Round History",
            font=("Segoe UI", 14, "bold"),
            fg=self.palette["text"],
            bg=self.palette["panel"],
        ).pack(anchor="w")

        self.history_list = tk.Listbox(
            right_panel,
            width=34,
            height=17,
            bg="#121A2D",
            fg=self.palette["text"],
            selectbackground="#314A7A",
            selectforeground=self.palette["text"],
            bd=0,
            highlightthickness=1,
            highlightbackground="#263A63",
            font=("Consolas", 10),
        )
        self.history_list.pack(pady=(10, 0), fill="both", expand=True)
        self.history_list.insert("end", "Welcome to Neon Arena")
        self.history_list.insert("end", "Your first round starts now")

    def _score_card(self, parent: tk.Frame, title: str, value: str, accent: str) -> tk.Label:
        card = tk.Frame(parent, bg=self.palette["panel"], padx=18, pady=14)
        card.pack(side="left", fill="x", expand=True, padx=4)

        tk.Label(
            card,
            text=title,
            fg=self.palette["muted"],
            bg=self.palette["panel"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            fg=accent,
            bg=self.palette["panel"],
            font=("Bahnschrift", 24, "bold"),
        )
        value_label.pack(anchor="w", pady=(4, 0))
        return value_label

    def _choice_button(self, parent: tk.Frame, text: str, value: str, bg_color: str) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg=self.palette["text"],
            activebackground=self.palette["accent_soft"],
            activeforeground=self.palette["text"],
            bd=0,
            relief="flat",
            pady=16,
            cursor="hand2",
            command=lambda v=value: self.play_round(v),
        )
        self._add_hover_effect(button, bg_color)
        self.choice_buttons.append(button)
        return button

    def _add_hover_effect(self, button: tk.Button, base_color: str) -> None:
        def on_enter(_: tk.Event) -> None:
            button.configure(bg=self.palette["accent_soft"])

        def on_leave(_: tk.Event) -> None:
            button.configure(bg=base_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _set_choice_buttons_state(self, enabled: bool) -> None:
        new_state = "normal" if enabled else "disabled"
        for button in self.choice_buttons:
            button.configure(state=new_state)

    def _pulse_result_box(self, color: str, index: int = 0) -> None:
        pulse_colors = [color, self.palette["panel_soft"],
                        color, self.palette["panel_soft"]]
        self.result_box.configure(bg=pulse_colors[index])
        self.result_label.configure(bg=pulse_colors[index])
        if index < len(pulse_colors) - 1:
            self.glow_job = self.root.after(
                80, self._pulse_result_box, color, index + 1)

    def play_round(self, user_pick: str) -> None:
        self._set_choice_buttons_state(False)
        self.result_label.configure(fg=self.palette["muted"])
        self.result_text.set("Computer is thinking...")
        self.round_text.set(
            f"Your move: {user_pick.upper()}     Computer: ...")
        self.root.after(320, self._resolve_round, user_pick)

    def _resolve_round(self, user_pick: str) -> None:
        computer_pick = random.choice(self.options)
        self.round_number += 1
        self.round_badge.configure(text=f"ROUND {self.round_number:02d}")

        if user_pick == computer_pick:
            result = "Tie"
            self.tie_score += 1
            color = self.palette["warning"]
            message = "Draw round. Same move from both sides."
        elif (
            (user_pick == "rock" and computer_pick == "scissors")
            or (user_pick == "paper" and computer_pick == "rock")
            or (user_pick == "scissors" and computer_pick == "paper")
        ):
            result = "Win"
            self.player_score += 1
            color = self.palette["accent"]
            message = "You win this round. Strong pick."
        else:
            result = "Loss"
            self.computer_score += 1
            color = self.palette["danger"]
            message = "Computer takes this round."

        if self.glow_job is not None:
            self.root.after_cancel(self.glow_job)
            self.glow_job = None

        self.result_label.configure(fg=color)
        self.result_text.set(message)
        self.round_text.set(
            f"Your move: {user_pick.upper()}     Computer: {computer_pick.upper()}"
        )
        self._pulse_result_box(color)

        self.player_score_value.configure(text=str(self.player_score))
        self.computer_score_value.configure(text=str(self.computer_score))
        self.tie_score_value.configure(text=str(self.tie_score))

        self.history_list.insert(
            0,
            f"{result:<4} | You: {user_pick:<8} CPU: {computer_pick:<8}",
        )
        if self.history_list.size() > 18:
            self.history_list.delete("end")

        self._set_choice_buttons_state(True)

    def reset_scores(self) -> None:
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.player_score_value.configure(text="0")
        self.computer_score_value.configure(text="0")
        self.tie_score_value.configure(text="0")
        self.round_number = 0
        self.round_badge.configure(text="ROUND 00")
        self.result_label.configure(fg=self.palette["text"])
        self.result_text.set("Scores reset. Choose your next move.")
        self.round_text.set("Your move: -     Computer: -")
        self.history_list.delete(0, "end")
        self.history_list.insert("end", "Scoreboard reset")


if __name__ == "__main__":
    app_root = tk.Tk()
    app = RockPaperScissorsApp(app_root)
    app_root.mainloop()
