import os
import subprocess
import sys
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox


@dataclass
class PhaseTarget:
    name: str
    subtitle: str
    script_path: str
    accent: str
    accent_soft: str
    description: str


class CosmicPhaseLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Cosmic Phase Launcher")
        self.root.geometry("1240x780")
        self.root.minsize(980, 640)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.targets = [
            PhaseTarget(
                name="Phase 1",
                subtitle="Core Utility Arena",
                script_path=os.path.join("Phase-1", "phase1.py"),
                accent="#F56B3A",
                accent_soft="#6B2F1B",
                description=(
                    "Launch the complete Phase-1 app collection: utilities, games, and "
                    "daily productivity tools in one place."
                ),
            ),
            PhaseTarget(
                name="Phase 2",
                subtitle="Puzzle and Logic Zone",
                script_path=os.path.join("Phase-2", "phase2.py"),
                accent="#1DC4A7",
                accent_soft="#1A574E",
                description=(
                    "Enter the advanced challenge lineup with puzzle-focused scripts, "
                    "reaction games, and solver projects."
                ),
            ),
        ]

        self.theme = {
            "bg": "#090E1B",
            "panel": "#101A34",
            "panel_alt": "#132144",
            "ink": "#F4F7FF",
            "muted": "#A8B4D6",
            "line": "#2B467A",
            "button_text": "#071522",
            "status_ok": "#8FF2C6",
            "status_warn": "#FFC091",
            "status_bad": "#FF8EA6",
        }

        self.status_var = tk.StringVar(value="Ready. Pick a phase and launch.")
        self.cards: list[tuple[tk.Frame,
                               dict[str, tk.Widget], PhaseTarget]] = []
        self.orb_phase = 0

        self._build_ui()
        self._tick_animation()

    def _build_ui(self) -> None:
        self.root.configure(bg=self.theme["bg"])

        self.backdrop = tk.Canvas(
            self.root,
            highlightthickness=0,
            relief="flat",
            bg=self.theme["bg"],
        )
        self.backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self._on_resize)
        self._draw_backdrop()

        shell = tk.Frame(self.root, bg=self.theme["bg"])
        shell.place(relx=0.5, rely=0.5, anchor="center",
                    relwidth=0.94, relheight=0.9)

        self._build_header(shell)
        self._build_cards(shell)
        self._build_footer(shell)

    def _build_header(self, parent: tk.Frame) -> None:
        header = tk.Frame(parent, bg=self.theme["bg"])
        header.pack(fill="x", pady=(0, 16))

        title_col = tk.Frame(header, bg=self.theme["bg"])
        title_col.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_col,
            text="COSMIC PHASE CONTROL",
            font=("Bahnschrift", 34, "bold"),
            fg=self.theme["ink"],
            bg=self.theme["bg"],
        ).pack(anchor="w")

        tk.Label(
            title_col,
            text="A high-aesthetic launch hub for Phase-1 and Phase-2.",
            font=("Segoe UI", 11),
            fg=self.theme["muted"],
            bg=self.theme["bg"],
        ).pack(anchor="w", pady=(4, 0))

        tk.Button(
            header,
            text="Open Workspace",
            font=("Segoe UI", 10, "bold"),
            bg="#294271",
            fg=self.theme["ink"],
            relief="flat",
            bd=0,
            padx=16,
            pady=9,
            cursor="hand2",
            activebackground="#355A98",
            activeforeground=self.theme["ink"],
            command=self._open_workspace,
        ).pack(side="right", anchor="ne", pady=(6, 0))

    def _build_cards(self, parent: tk.Frame) -> None:
        area = tk.Frame(parent, bg=self.theme["bg"])
        area.pack(fill="both", expand=True)

        for target in self.targets:
            card, widgets = self._make_card(area, target)
            card.pack(side="left", fill="both", expand=True, padx=10)
            self.cards.append((card, widgets, target))

    def _make_card(self, parent: tk.Frame, target: PhaseTarget) -> tuple[tk.Frame, dict[str, tk.Widget]]:
        card = tk.Frame(
            parent,
            bg=self.theme["panel"],
            padx=20,
            pady=20,
            highlightthickness=1,
            highlightbackground=self.theme["line"],
            highlightcolor=self.theme["line"],
        )

        badge = tk.Label(
            card,
            text=target.subtitle,
            font=("Segoe UI", 9, "bold"),
            fg="#FFE5D8" if target.name == "Phase 1" else "#D9FFF7",
            bg=target.accent_soft,
            padx=10,
            pady=4,
        )
        badge.pack(anchor="w")

        title = tk.Label(
            card,
            text=target.name,
            font=("Bahnschrift", 28, "bold"),
            fg=self.theme["ink"],
            bg=self.theme["panel"],
        )
        title.pack(anchor="w", pady=(14, 6))

        desc = tk.Label(
            card,
            text=target.description,
            font=("Segoe UI", 10),
            fg=self.theme["muted"],
            bg=self.theme["panel"],
            justify="left",
            wraplength=470,
        )
        desc.pack(anchor="w")

        path_chip = tk.Label(
            card,
            text=f"script: {target.script_path}",
            font=("Consolas", 9),
            fg="#CFE2FF",
            bg=self.theme["panel_alt"],
            padx=10,
            pady=5,
        )
        path_chip.pack(anchor="w", pady=(14, 14))

        launch_btn = tk.Button(
            card,
            text="Launch",
            font=("Segoe UI", 12, "bold"),
            bg=target.accent,
            fg=self.theme["button_text"],
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            activebackground=self._brighten(target.accent),
            activeforeground=self.theme["button_text"],
            command=lambda t=target: self._launch_target(t),
        )
        launch_btn.pack(anchor="w")

        widget_map = {
            "title": title,
            "desc": desc,
            "badge": badge,
            "chip": path_chip,
            "button": launch_btn,
        }

        self._bind_card_hover(card, widget_map)
        return card, widget_map

    def _bind_card_hover(self, card: tk.Frame, widgets: dict[str, tk.Widget]) -> None:
        def on_enter(_event=None) -> None:
            card.configure(
                bg=self.theme["panel_alt"],
                highlightbackground="#4D73BD",
                highlightcolor="#4D73BD",
            )
            for key, widget in widgets.items():
                if key in {"title", "desc"}:
                    widget.configure(bg=self.theme["panel_alt"])

        def on_leave(_event=None) -> None:
            card.configure(
                bg=self.theme["panel"],
                highlightbackground=self.theme["line"],
                highlightcolor=self.theme["line"],
            )
            for key, widget in widgets.items():
                if key in {"title", "desc"}:
                    widget.configure(bg=self.theme["panel"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        widgets["button"].bind("<Enter>", on_enter)
        widgets["button"].bind("<Leave>", on_leave)

    def _build_footer(self, parent: tk.Frame) -> None:
        footer = tk.Frame(parent, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(14, 0))

        chip = tk.Label(
            footer,
            text="launcher.py",
            font=("Consolas", 9),
            fg="#FFDFC7",
            bg="#543729",
            padx=10,
            pady=5,
        )
        chip.pack(side="left")

        tk.Label(
            footer,
            textvariable=self.status_var,
            font=("Consolas", 10),
            fg=self.theme["muted"],
            bg=self.theme["bg"],
        ).pack(side="right")

    def _launch_target(self, target: PhaseTarget) -> None:
        full_path = os.path.join(self.base_dir, target.script_path)

        if not os.path.exists(full_path):
            messagebox.showerror(
                "Missing Script",
                f"Could not find script:\n{target.script_path}",
            )
            self.status_var.set(f"Missing: {target.script_path}")
            return

        try:
            subprocess.Popen([sys.executable, full_path], cwd=self.base_dir)
            self.status_var.set(f"Launched {target.name} frontend.")
        except Exception as exc:
            messagebox.showerror(
                "Launch Error",
                f"Could not launch {target.name}.\n\n{exc}",
            )
            self.status_var.set(f"Launch failed for {target.name}.")

    def _open_workspace(self) -> None:
        try:
            os.startfile(self.base_dir)
            self.status_var.set("Workspace opened in file explorer.")
        except Exception as exc:
            messagebox.showerror("Open Folder Error",
                                 f"Could not open workspace.\n\n{exc}")
            self.status_var.set("Failed to open workspace folder.")

    def _on_resize(self, _event: tk.Event) -> None:
        self._draw_backdrop()

    def _draw_backdrop(self) -> None:
        self.backdrop.delete("all")
        width = max(self.root.winfo_width(), 1)
        height = max(self.root.winfo_height(), 1)

        self.backdrop.create_rectangle(
            0, 0, width, height, fill=self.theme["bg"], outline="")

        self.backdrop.create_oval(-260, -210, width *
                                  0.50, height * 0.54, fill="#243F76", outline="")
        self.backdrop.create_oval(
            width * 0.48, -220, width + 260, height * 0.48, fill="#5D2A50", outline="")
        self.backdrop.create_oval(
            width * 0.16, height * 0.36, width + 300, height + 220, fill="#163364", outline="")

        orb_x = width * 0.78 + (18 * ((self.orb_phase % 20) - 10) / 10)
        self.backdrop.create_oval(
            orb_x, height * 0.68, orb_x + 95, height * 0.82, fill="#FF8D61", outline="")

    def _tick_animation(self) -> None:
        self.orb_phase = (self.orb_phase + 1) % 20
        self._draw_backdrop()
        self.root.after(85, self._tick_animation)

    def _brighten(self, color: str) -> str:
        color = color.lstrip("#")
        if len(color) != 6:
            return "#FFFFFF"

        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        r = min(255, r + 28)
        g = min(255, g + 28)
        b = min(255, b + 28)
        return f"#{r:02X}{g:02X}{b:02X}"


if __name__ == "__main__":
    root = tk.Tk()
    CosmicPhaseLauncher(root)
    root.mainloop()
