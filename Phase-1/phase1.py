import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


APPS = [
    {
        "title": "Digital Clock",
        "file": "clock.py",
        "tag": "Utility",
        "emoji": "⏰",
        "description": "Live time and date display with a clean Tkinter layout.",
    },
    {
        "title": "Hotel Menu",
        "file": "hotelmenu.py",
        "tag": "Billing",
        "emoji": "🍽",
        "description": "Restaurant order and bill generator with itemized pricing.",
    },
    {
        "title": "Rent Splitter",
        "file": "rent.py",
        "tag": "Finance",
        "emoji": "🏠",
        "description": "Split rent, food and electricity cost among flatmates.",
    },
    {
        "title": "Rock Paper Scissors",
        "file": "rock_paper_scissors.py",
        "tag": "Game",
        "emoji": "🎮",
        "description": "Neon-styled player vs computer arena challenge.",
    },
    {
        "title": "Tic Tac Toe",
        "file": "tic_tac_toe.py",
        "tag": "Game",
        "emoji": "❌",
        "description": "Classic 2-player tic tac toe experience.",
    },
    {
        "title": "TaskFlow To-Do",
        "file": "to_do.py",
        "tag": "Productivity",
        "emoji": "✅",
        "description": "Task manager with add, update, done and delete actions.",
    },
]


class PhaseOneLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Phase-1 Aura Launcher")
        self.root.geometry("1220x760")
        self.root.minsize(1080, 680)

        self.palette = {
            "bg": "#0B1020",
            "bg_soft": "#101833",
            "surface": "#121D3A",
            "surface_alt": "#16264A",
            "ink": "#EAF2FF",
            "muted": "#93A4C8",
            "primary": "#35E0C5",
            "primary_hover": "#22C8AD",
            "accent": "#FFBA5A",
            "danger": "#FF6F91",
            "line": "#27406D",
            "chip": "#22355F",
        }

        self.cards: list[dict[str, tk.Widget]] = []
        self.filtered_apps = APPS
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready. Pick an app and launch.")

        self._build_ui()
        self._render_cards(self.filtered_apps)

    def _build_ui(self) -> None:
        self.root.configure(bg=self.palette["bg"])

        backdrop = tk.Canvas(self.root, highlightthickness=0,
                             relief="flat", bg=self.palette["bg"])
        backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)
        backdrop.create_oval(-260, -240, 440, 360, fill="#193566", outline="")
        backdrop.create_oval(680, -260, 1400, 360, fill="#204876", outline="")
        backdrop.create_oval(280, 360, 1320, 1100, fill="#102A53", outline="")

        shell = tk.Frame(self.root, bg=self.palette["bg"])
        shell.place(relx=0.5, rely=0.5, anchor="center",
                    relwidth=0.95, relheight=0.93)

        self._build_header(shell)
        self._build_grid_area(shell)
        self._build_footer(shell)

    def _build_header(self, parent: tk.Frame) -> None:
        header = tk.Frame(parent, bg=self.palette["bg"])
        header.pack(fill="x", pady=(0, 14))

        title_col = tk.Frame(header, bg=self.palette["bg"])
        title_col.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_col,
            text="PHASE-1 AURA+ FRONTEND",
            font=("Bahnschrift", 30, "bold"),
            fg=self.palette["ink"],
            bg=self.palette["bg"],
        ).pack(anchor="w")

        tk.Label(
            title_col,
            text="A premium launcher for all Phase-1 Python apps.",
            font=("Segoe UI", 11),
            fg=self.palette["muted"],
            bg=self.palette["bg"],
        ).pack(anchor="w", pady=(4, 0))

        actions = tk.Frame(header, bg=self.palette["bg"])
        actions.pack(side="right", anchor="ne", pady=(5, 0))

        search_box = tk.Entry(
            actions,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg="#0F1A35",
            fg=self.palette["ink"],
            insertbackground=self.palette["ink"],
            relief="flat",
            bd=0,
            width=30,
        )
        search_box.pack(side="left", ipady=8, ipadx=10)
        search_box.bind("<KeyRelease>", lambda _e: self._filter_apps())

        clear_btn = tk.Button(
            actions,
            text="Clear",
            font=("Segoe UI", 10, "bold"),
            bg="#29406C",
            fg=self.palette["ink"],
            activebackground="#33568D",
            activeforeground=self.palette["ink"],
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            command=self._clear_search,
        )
        clear_btn.pack(side="left", padx=(8, 0))

    def _build_grid_area(self, parent: tk.Frame) -> None:
        grid_wrap = tk.Frame(parent, bg=self.palette["bg"])
        grid_wrap.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            grid_wrap,
            bg=self.palette["bg"],
            highlightthickness=0,
            relief="flat",
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            grid_wrap, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.content_frame = tk.Frame(self.canvas, bg=self.palette["bg"])
        self.content_window = self.canvas.create_window(
            (0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self._sync_scrollregion)
        self.canvas.bind("<Configure>", self._resize_canvas_window)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _build_footer(self, parent: tk.Frame) -> None:
        footer = tk.Frame(parent, bg=self.palette["bg"])
        footer.pack(fill="x", pady=(12, 0))

        chip = tk.Frame(footer, bg=self.palette["chip"], padx=12, pady=7)
        chip.pack(side="left")
        tk.Label(
            chip,
            text="Phase-1 Collection",
            font=("Segoe UI", 9, "bold"),
            bg=self.palette["chip"],
            fg=self.palette["accent"],
        ).pack()

        tk.Label(
            footer,
            textvariable=self.status_var,
            font=("Consolas", 10),
            fg=self.palette["muted"],
            bg=self.palette["bg"],
        ).pack(side="right")

    def _sync_scrollregion(self, _event=None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas_window(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.content_window, width=event.width)

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _clear_search(self) -> None:
        self.search_var.set("")
        self._filter_apps()

    def _filter_apps(self) -> None:
        query = self.search_var.get().strip().lower()
        if not query:
            self.filtered_apps = APPS
        else:
            self.filtered_apps = [
                app
                for app in APPS
                if query in app["title"].lower()
                or query in app["tag"].lower()
                or query in app["file"].lower()
            ]

        self._render_cards(self.filtered_apps)
        self.status_var.set(f"Showing {len(self.filtered_apps)} app(s).")

    def _render_cards(self, apps: list[dict]) -> None:
        for child in self.content_frame.winfo_children():
            child.destroy()

        self.cards.clear()

        if not apps:
            empty = tk.Frame(self.content_frame,
                             bg=self.palette["surface"], padx=24, pady=24)
            empty.pack(fill="x", pady=24)
            tk.Label(
                empty,
                text="No apps matched your search.",
                font=("Segoe UI", 14, "bold"),
                fg=self.palette["ink"],
                bg=self.palette["surface"],
            ).pack(anchor="w")
            tk.Label(
                empty,
                text="Try searching by title, tag, or file name.",
                font=("Segoe UI", 10),
                fg=self.palette["muted"],
                bg=self.palette["surface"],
            ).pack(anchor="w", pady=(6, 0))
            return

        row = None
        for index, app in enumerate(apps):
            if index % 2 == 0:
                row = tk.Frame(self.content_frame, bg=self.palette["bg"])
                row.pack(fill="x", pady=8)

            if row is None:
                continue

            card = self._build_card(row, app)
            card.pack(side="left", fill="both", expand=True, padx=8)

    def _build_card(self, parent: tk.Frame, app: dict) -> tk.Frame:
        card = tk.Frame(
            parent, bg=self.palette["surface"], padx=16, pady=16, highlightthickness=1)
        card.configure(
            highlightbackground=self.palette["line"], highlightcolor=self.palette["line"])

        top = tk.Frame(card, bg=self.palette["surface"])
        top.pack(fill="x")

        tk.Label(
            top,
            text=app["emoji"],
            font=("Segoe UI Emoji", 18),
            fg=self.palette["ink"],
            bg=self.palette["surface"],
        ).pack(side="left")

        tk.Label(
            top,
            text=app["tag"],
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["accent"],
            bg=self.palette["chip"],
            padx=8,
            pady=4,
        ).pack(side="right")

        tk.Label(
            card,
            text=app["title"],
            font=("Segoe UI", 16, "bold"),
            fg=self.palette["ink"],
            bg=self.palette["surface"],
        ).pack(anchor="w", pady=(10, 4))

        tk.Label(
            card,
            text=app["description"],
            font=("Segoe UI", 10),
            fg=self.palette["muted"],
            bg=self.palette["surface"],
            justify="left",
            wraplength=430,
        ).pack(anchor="w")

        file_chip = tk.Label(
            card,
            text=f"file: {app['file']}",
            font=("Consolas", 9),
            fg="#B4C7E9",
            bg=self.palette["surface_alt"],
            padx=8,
            pady=4,
        )
        file_chip.pack(anchor="w", pady=(12, 12))

        btn = tk.Button(
            card,
            text="Launch",
            font=("Segoe UI", 10, "bold"),
            bg=self.palette["primary"],
            fg="#053731",
            activebackground=self.palette["primary_hover"],
            activeforeground="#042A26",
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            command=lambda f=app["file"], t=app["title"]: self._launch_app(
                f, t),
        )
        btn.pack(anchor="w")

        self._add_card_hover(card, btn)
        return card

    def _add_card_hover(self, card: tk.Frame, btn: tk.Button) -> None:
        def on_enter(_event=None) -> None:
            card.configure(
                bg=self.palette["surface_alt"], highlightbackground="#3E66A6", highlightcolor="#3E66A6")
            for child in card.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=self.palette["surface_alt"])
                    for inner in child.winfo_children():
                        try:
                            if inner.cget("bg") == self.palette["surface"]:
                                inner.configure(bg=self.palette["surface_alt"])
                        except tk.TclError:
                            continue
                else:
                    try:
                        if child.cget("bg") == self.palette["surface"]:
                            child.configure(bg=self.palette["surface_alt"])
                    except tk.TclError:
                        continue

        def on_leave(_event=None) -> None:
            card.configure(
                bg=self.palette["surface"], highlightbackground=self.palette["line"], highlightcolor=self.palette["line"])
            for child in card.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=self.palette["surface"])
                    for inner in child.winfo_children():
                        try:
                            if inner.cget("bg") == self.palette["surface_alt"]:
                                inner.configure(bg=self.palette["surface"])
                        except tk.TclError:
                            continue
                else:
                    try:
                        if child.cget("bg") == self.palette["surface_alt"]:
                            child.configure(bg=self.palette["surface"])
                    except tk.TclError:
                        continue

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _launch_app(self, file_name: str, title: str) -> None:
        script_path = os.path.join(os.path.dirname(__file__), file_name)

        if not os.path.exists(script_path):
            messagebox.showerror(
                "Missing File", f"Could not find {file_name}.")
            self.status_var.set(f"Error: {file_name} not found.")
            return

        try:
            subprocess.Popen([sys.executable, script_path],
                             cwd=os.path.dirname(__file__))
            self.status_var.set(f"Launched {title}.")
        except Exception as exc:
            messagebox.showerror(
                "Launch Error", f"Could not launch {title}.\n\n{exc}")
            self.status_var.set(f"Launch failed for {title}.")


if __name__ == "__main__":
    app_root = tk.Tk()
    PhaseOneLauncher(app_root)
    app_root.mainloop()
