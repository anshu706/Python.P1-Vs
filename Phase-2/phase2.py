import os
import subprocess
import sys
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox


@dataclass
class ScriptItem:
    title: str
    file_name: str
    description: str
    category: str


class PhaseTwoFrontend:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Phase-2 Crimson Cobalt Frontend")
        self.root.geometry("1260x800")
        self.root.minsize(1080, 700)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(self.base_dir).lower() == "phase-2":
            self.phase_two_dir = self.base_dir
        else:
            self.phase_two_dir = os.path.join(self.base_dir, "Phase-2")

        self.palette = {
            "bg": "#080D1C",
            "bg_soft": "#0E1630",
            "surface": "#111D3D",
            "surface_alt": "#162752",
            "ink": "#EEF3FF",
            "muted": "#9FB0D8",
            "line": "#26498A",
            "red": "#FF4C6D",
            "red_hover": "#FF6A84",
            "blue": "#4DB0FF",
            "blue_hover": "#7AC4FF",
            "chip": "#203C73",
            "chip_alt": "#52223E",
            "ok": "#90F0BF",
        }

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready. Pick a script to launch.")
        self.script_count_var = tk.StringVar(value="0 scripts")

        self.cards: list[tk.Frame] = []
        self.all_scripts: list[ScriptItem] = []
        self.filtered_scripts: list[ScriptItem] = []

        self._build_ui()
        self._refresh_scripts()

    def _build_ui(self) -> None:
        self.root.configure(bg=self.palette["bg"])

        self.backdrop = tk.Canvas(
            self.root,
            highlightthickness=0,
            relief="flat",
            bg=self.palette["bg"],
        )
        self.backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._draw_backdrop()
        self.root.bind("<Configure>", self._on_window_resize)

        shell = tk.Frame(self.root, bg=self.palette["bg"])
        shell.place(relx=0.5, rely=0.5, anchor="center",
                    relwidth=0.95, relheight=0.93)

        self._build_header(shell)
        self._build_grid(shell)
        self._build_footer(shell)

    def _draw_backdrop(self) -> None:
        self.backdrop.delete("all")

        width = max(1, self.root.winfo_width())
        height = max(1, self.root.winfo_height())

        self.backdrop.create_rectangle(
            0, 0, width, height, fill=self.palette["bg"], outline="")
        self.backdrop.create_oval(-280, -260, width *
                                  0.52, height * 0.55, fill="#1A2D62", outline="")
        self.backdrop.create_oval(
            width * 0.45, -230, width + 300, height * 0.50, fill="#5A1D45", outline="")
        self.backdrop.create_oval(
            width * 0.15, height * 0.35, width + 220, height + 260, fill="#102757", outline="")
        self.backdrop.create_oval(-220, height * 0.52, width *
                                  0.45, height + 320, fill="#471D4A", outline="")

    def _on_window_resize(self, _event: tk.Event) -> None:
        self._draw_backdrop()

    def _build_header(self, parent: tk.Frame) -> None:
        header = tk.Frame(parent, bg=self.palette["bg"])
        header.pack(fill="x", pady=(0, 14))

        left = tk.Frame(header, bg=self.palette["bg"])
        left.pack(side="left", fill="x", expand=True)

        tk.Label(
            left,
            text="PHASE-2 SCRIPT VAULT",
            font=("Bahnschrift", 33, "bold"),
            fg=self.palette["ink"],
            bg=self.palette["bg"],
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Aesthetic red and blue frontend for all Phase-2 files.",
            font=("Segoe UI", 11),
            fg=self.palette["muted"],
            bg=self.palette["bg"],
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(header, bg=self.palette["bg"])
        right.pack(side="right", anchor="ne", pady=(4, 0))

        self.search_entry = tk.Entry(
            right,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg="#0C1330",
            fg=self.palette["ink"],
            insertbackground=self.palette["ink"],
            relief="flat",
            bd=0,
            width=30,
        )
        self.search_entry.pack(side="left", ipady=8, ipadx=10)
        self.search_entry.bind(
            "<KeyRelease>", lambda _e: self._filter_scripts())

    def _build_grid(self, parent: tk.Frame) -> None:
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

        chip_left = tk.Frame(footer, bg=self.palette["chip"], padx=12, pady=7)
        chip_left.pack(side="left")
        tk.Label(
            chip_left,
            textvariable=self.script_count_var,
            font=("Segoe UI", 9, "bold"),
            bg=self.palette["chip"],
            fg=self.palette["blue"],
        ).pack()

        chip_mid = tk.Frame(
            footer, bg=self.palette["chip_alt"], padx=12, pady=7)
        chip_mid.pack(side="left", padx=(8, 0))
        tk.Button(
            chip_mid,
            text="Open Phase-2 Folder",
            font=("Segoe UI", 9, "bold"),
            bg=self.palette["chip_alt"],
            fg="#FFB9CB",
            relief="flat",
            bd=0,
            activebackground="#642A4D",
            activeforeground="#FFD3DE",
            cursor="hand2",
            command=self._open_phase_two_folder,
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

    def _open_phase_two_folder(self) -> None:
        if not os.path.isdir(self.phase_two_dir):
            messagebox.showerror(
                "Folder Missing", "Phase-2 folder was not found.")
            self.status_var.set("Error: Phase-2 folder missing.")
            return

        try:
            os.startfile(self.phase_two_dir)
            self.status_var.set("Opened Phase-2 folder.")
        except Exception as exc:
            messagebox.showerror("Open Folder Error",
                                 f"Could not open Phase-2 folder.\n\n{exc}")
            self.status_var.set("Failed to open Phase-2 folder.")

    def _refresh_scripts(self) -> None:
        if not os.path.isdir(self.phase_two_dir):
            messagebox.showerror(
                "Folder Missing", "Phase-2 folder does not exist in this workspace.")
            self.all_scripts = []
            self.filtered_scripts = []
            self._render_cards([])
            self.script_count_var.set("0 scripts")
            self.status_var.set("Phase-2 folder missing.")
            return

        names = [
            name
            for name in os.listdir(self.phase_two_dir)
            if name.endswith(".py")
            and not name.startswith("__")
            and name.lower() != "phase2.py"
        ]
        names.sort()

        self.all_scripts = [self._make_script_item(name) for name in names]
        self.filtered_scripts = self.all_scripts

        self._render_cards(self.filtered_scripts)
        self.script_count_var.set(f"{len(self.all_scripts)} scripts")
        self.status_var.set("Phase-2 scripts refreshed.")

    def _make_script_item(self, file_name: str) -> ScriptItem:
        title = file_name.replace(".py", "").replace("_", " ").title()
        category = self._guess_category(file_name)
        description = self._build_description(file_name)
        return ScriptItem(title=title, file_name=file_name, description=description, category=category)

    def _guess_category(self, file_name: str) -> str:
        key = file_name.lower()
        if "sudoku" in key or "minesweeper" in key or "mastermind" in key:
            return "Logic"
        if "slot" in key:
            return "Arcade"
        if "guess" in key:
            return "Classic"
        if "aim" in key:
            return "Skill"
        return "Python"

    def _build_description(self, file_name: str) -> str:
        descriptions = {
            "aim_trainer.py": "Precision reaction trainer with timing-focused gameplay.",
            "guess_number.py": "Number guessing challenge with hint-driven rounds.",
            "mastermind_game.py": "Code-breaking puzzle where logic beats luck.",
            "minesweeper.py": "Grid puzzle adventure with risk and deduction.",
            "slot_machine.py": "Casino-style spinning reels and rewards.",
            "sudoku_solver.py": "Automatic Sudoku solving with algorithmic logic.",
        }
        return descriptions.get(file_name, "Phase-2 script ready to launch from this frontend.")

    def _filter_scripts(self) -> None:
        query = self.search_var.get().strip().lower()

        if not query:
            self.filtered_scripts = self.all_scripts
        else:
            self.filtered_scripts = [
                script
                for script in self.all_scripts
                if query in script.title.lower()
                or query in script.file_name.lower()
                or query in script.category.lower()
            ]

        self._render_cards(self.filtered_scripts)
        self.status_var.set(f"Showing {len(self.filtered_scripts)} script(s).")

    def _render_cards(self, scripts: list[ScriptItem]) -> None:
        for child in self.content_frame.winfo_children():
            child.destroy()

        self.cards.clear()

        if not scripts:
            empty = tk.Frame(self.content_frame,
                             bg=self.palette["surface"], padx=24, pady=24)
            empty.pack(fill="x", pady=24)

            tk.Label(
                empty,
                text="No files matched your search.",
                font=("Segoe UI", 15, "bold"),
                fg=self.palette["ink"],
                bg=self.palette["surface"],
            ).pack(anchor="w")
            tk.Label(
                empty,
                text="Try searching by file name, title, or category.",
                font=("Segoe UI", 10),
                fg=self.palette["muted"],
                bg=self.palette["surface"],
            ).pack(anchor="w", pady=(6, 0))
            return

        row = None
        for idx, script in enumerate(scripts):
            if idx % 2 == 0:
                row = tk.Frame(self.content_frame, bg=self.palette["bg"])
                row.pack(fill="x", pady=8)

            if row is None:
                continue

            card = self._build_card(row, script)
            card.pack(side="left", fill="both", expand=True, padx=8)

    def _build_card(self, parent: tk.Frame, script: ScriptItem) -> tk.Frame:
        card = tk.Frame(
            parent, bg=self.palette["surface"], padx=16, pady=16, highlightthickness=1)
        card.configure(
            highlightbackground=self.palette["line"], highlightcolor=self.palette["line"])

        top = tk.Frame(card, bg=self.palette["surface"])
        top.pack(fill="x")

        tk.Label(
            top,
            text=script.category,
            font=("Segoe UI", 9, "bold"),
            fg="#D4E6FF",
            bg=self.palette["chip"],
            padx=8,
            pady=4,
        ).pack(side="left")

        tk.Label(
            top,
            text="phase-2",
            font=("Consolas", 9),
            fg="#FFD2DC",
            bg=self.palette["chip_alt"],
            padx=8,
            pady=4,
        ).pack(side="right")

        tk.Label(
            card,
            text=script.title,
            font=("Segoe UI", 16, "bold"),
            fg=self.palette["ink"],
            bg=self.palette["surface"],
        ).pack(anchor="w", pady=(10, 4))

        tk.Label(
            card,
            text=script.description,
            font=("Segoe UI", 10),
            fg=self.palette["muted"],
            bg=self.palette["surface"],
            justify="left",
            wraplength=430,
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"file: {script.file_name}",
            font=("Consolas", 9),
            fg="#CAE3FF",
            bg=self.palette["surface_alt"],
            padx=8,
            pady=4,
        ).pack(anchor="w", pady=(12, 12))

        buttons = tk.Frame(card, bg=self.palette["surface"])
        buttons.pack(anchor="w")

        launch_btn = tk.Button(
            buttons,
            text="Launch",
            font=("Segoe UI", 10, "bold"),
            bg=self.palette["blue"],
            fg="#04243D",
            activebackground=self.palette["blue_hover"],
            activeforeground="#02213A",
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            command=lambda name=script.file_name, title=script.title: self._launch_script(
                name, title),
        )
        launch_btn.pack(side="left")

        self._add_hover(card)
        return card

    def _add_hover(self, card: tk.Frame) -> None:
        def on_enter(_event=None) -> None:
            card.configure(
                bg=self.palette["surface_alt"],
                highlightbackground="#4D7ACC",
                highlightcolor="#4D7ACC",
            )
            for child in card.winfo_children():
                self._swap_background(
                    child, self.palette["surface"], self.palette["surface_alt"])

        def on_leave(_event=None) -> None:
            card.configure(
                bg=self.palette["surface"],
                highlightbackground=self.palette["line"],
                highlightcolor=self.palette["line"],
            )
            for child in card.winfo_children():
                self._swap_background(
                    child, self.palette["surface_alt"], self.palette["surface"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def _swap_background(self, widget: tk.Widget, old: str, new: str) -> None:
        try:
            if widget.cget("bg") == old:
                widget.configure(bg=new)
        except tk.TclError:
            return

        for child in widget.winfo_children():
            self._swap_background(child, old, new)

    def _launch_script(self, file_name: str, title: str) -> None:
        script_path = os.path.join(self.phase_two_dir, file_name)

        if not os.path.exists(script_path):
            messagebox.showerror(
                "Missing File", f"Could not find {file_name}.")
            self.status_var.set(f"Error: {file_name} not found.")
            return

        try:
            subprocess.Popen([sys.executable, script_path],
                             cwd=self.phase_two_dir)
            self.status_var.set(f"Launched {title}.")
        except Exception as exc:
            messagebox.showerror(
                "Launch Error", f"Could not launch {title}.\n\n{exc}")
            self.status_var.set(f"Launch failed for {title}.")


if __name__ == "__main__":
    root_app = tk.Tk()
    PhaseTwoFrontend(root_app)
    root_app.mainloop()
