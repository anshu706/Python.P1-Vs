import datetime
import tkinter as tk
from tkinter import messagebox


class TodoFrontendApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("TaskFlow Studio")
        self.root.geometry("980x640")
        self.root.minsize(880, 560)

        self.palette = {
            "bg": "#0F172A",
            "panel": "#111C38",
            "panel_soft": "#1B2A4D",
            "surface": "#0B1328",
            "primary": "#2DD4BF",
            "primary_hover": "#15B8A1",
            "secondary": "#FDBA74",
            "danger": "#FB7185",
            "text": "#ECF3FF",
            "muted": "#98A8C7",
        }

        self.tasks: list[dict[str, bool | str]] = []
        self.selected_index: int | None = None
        self.buttons: list[tk.Button] = []

        self._build_ui()
        self._refresh_clock()

    def _build_ui(self) -> None:
        self.root.configure(bg=self.palette["bg"])

        backdrop = tk.Canvas(
            self.root,
            bg=self.palette["bg"],
            highlightthickness=0,
            relief="flat",
        )
        backdrop.place(relx=0, rely=0, relwidth=1, relheight=1)
        backdrop.create_oval(-220, -220, 260, 260, fill="#17315C", outline="")
        backdrop.create_oval(680, -240, 1180, 300, fill="#10345A", outline="")
        backdrop.create_oval(340, 390, 1060, 1020, fill="#102949", outline="")

        shell = tk.Frame(self.root, bg=self.palette["bg"])
        shell.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.9)

        header = tk.Frame(shell, bg=self.palette["bg"])
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="TASKFLOW STUDIO",
            font=("Bahnschrift", 28, "bold"),
            fg=self.palette["text"],
            bg=self.palette["bg"],
        ).pack(side="left")

        self.clock_label = tk.Label(
            header,
            font=("Consolas", 11, "bold"),
            fg=self.palette["secondary"],
            bg=self.palette["bg"],
            text="",
        )
        self.clock_label.pack(side="right")

        stats_row = tk.Frame(shell, bg=self.palette["bg"])
        stats_row.pack(fill="x", pady=(0, 16))

        self.total_value = self._stat_card(stats_row, "TOTAL", "0", self.palette["secondary"])
        self.done_value = self._stat_card(stats_row, "DONE", "0", self.palette["primary"])
        self.pending_value = self._stat_card(stats_row, "PENDING", "0", self.palette["danger"])

        body = tk.Frame(shell, bg=self.palette["bg"])
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=self.palette["panel"], padx=22, pady=22)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(body, bg=self.palette["panel"], padx=20, pady=20)
        right.pack(side="right", fill="y", padx=(10, 0))

        tk.Label(
            left,
            text="Create and Manage Tasks",
            font=("Segoe UI", 17, "bold"),
            fg=self.palette["text"],
            bg=self.palette["panel"],
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Select a task to edit or complete it. Keep your day intentionally organized.",
            font=("Segoe UI", 10),
            fg=self.palette["muted"],
            bg=self.palette["panel"],
            wraplength=520,
            justify="left",
        ).pack(anchor="w", pady=(5, 14))

        input_row = tk.Frame(left, bg=self.palette["panel"])
        input_row.pack(fill="x")

        self.task_entry = tk.Entry(
            input_row,
            font=("Segoe UI", 12),
            bg=self.palette["surface"],
            fg=self.palette["text"],
            insertbackground=self.palette["text"],
            relief="flat",
            bd=0,
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.task_entry.bind("<Return>", lambda _: self.add_task())

        add_button = self._action_button(
            input_row,
            text="ADD",
            bg=self.palette["primary"],
            hover=self.palette["primary_hover"],
            command=self.add_task,
            text_color="#062A27",
        )
        add_button.pack(side="right", padx=(8, 0), ipadx=14, ipady=8)

        button_row = tk.Frame(left, bg=self.palette["panel"])
        button_row.pack(fill="x", pady=(12, 14))

        update_button = self._action_button(
            button_row,
            text="Update",
            bg="#2E4B77",
            hover="#3C6299",
            command=self.update_task,
            text_color=self.palette["text"],
        )
        update_button.pack(side="left", fill="x", expand=True, padx=(0, 6), ipady=8)

        done_button = self._action_button(
            button_row,
            text="Toggle Done",
            bg="#2A5B54",
            hover="#327068",
            command=self.toggle_done,
            text_color=self.palette["text"],
        )
        done_button.pack(side="left", fill="x", expand=True, padx=6, ipady=8)

        delete_button = self._action_button(
            button_row,
            text="Delete",
            bg="#63354A",
            hover="#7B435C",
            command=self.delete_task,
            text_color=self.palette["text"],
        )
        delete_button.pack(side="left", fill="x", expand=True, padx=(6, 0), ipady=8)

        self.task_list = tk.Listbox(
            left,
            bg="#0C1731",
            fg=self.palette["text"],
            selectbackground="#25457A",
            selectforeground=self.palette["text"],
            highlightthickness=1,
            highlightbackground="#2B4371",
            bd=0,
            font=("Consolas", 11),
        )
        self.task_list.pack(fill="both", expand=True)
        self.task_list.bind("<<ListboxSelect>>", self.on_task_select)

        footer_row = tk.Frame(left, bg=self.palette["panel"])
        footer_row.pack(fill="x", pady=(12, 0))

        clear_button = self._action_button(
            footer_row,
            text="Clear All",
            bg="#3C2C58",
            hover="#4F3A73",
            command=self.clear_all,
            text_color=self.palette["text"],
        )
        clear_button.pack(side="right", ipady=8, ipadx=12)

        tk.Label(
            right,
            text="Quick Tips",
            font=("Segoe UI", 14, "bold"),
            fg=self.palette["text"],
            bg=self.palette["panel"],
        ).pack(anchor="w")

        tips = [
            "Press Enter to add quickly",
            "Select a task before update/delete",
            "Use Toggle Done to mark progress",
            "Clear All to restart your board",
        ]
        for tip in tips:
            tk.Label(
                right,
                text=f"- {tip}",
                font=("Segoe UI", 10),
                fg=self.palette["muted"],
                bg=self.palette["panel"],
                justify="left",
            ).pack(anchor="w", pady=5)

        tk.Label(
            right,
            text="Status Legend",
            font=("Segoe UI", 12, "bold"),
            fg=self.palette["secondary"],
            bg=self.palette["panel"],
        ).pack(anchor="w", pady=(18, 6))

        tk.Label(
            right,
            text="[ ] Pending",
            font=("Consolas", 10),
            fg=self.palette["danger"],
            bg=self.palette["panel"],
        ).pack(anchor="w")
        tk.Label(
            right,
            text="[x] Completed",
            font=("Consolas", 10),
            fg=self.palette["primary"],
            bg=self.palette["panel"],
        ).pack(anchor="w", pady=(4, 0))

    def _stat_card(self, parent: tk.Frame, title: str, value: str, accent: str) -> tk.Label:
        card = tk.Frame(parent, bg=self.palette["panel"], padx=18, pady=14)
        card.pack(side="left", fill="x", expand=True, padx=4)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["muted"],
            bg=self.palette["panel"],
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Bahnschrift", 24, "bold"),
            fg=accent,
            bg=self.palette["panel"],
        )
        value_label.pack(anchor="w", pady=(4, 0))
        return value_label

    def _action_button(
        self,
        parent: tk.Frame,
        text: str,
        bg: str,
        hover: str,
        command,
        text_color: str,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=text_color,
            activebackground=hover,
            activeforeground=text_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command,
        )

        def on_enter(_: tk.Event) -> None:
            button.configure(bg=hover)

        def on_leave(_: tk.Event) -> None:
            button.configure(bg=bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        self.buttons.append(button)
        return button

    def _refresh_clock(self) -> None:
        now = datetime.datetime.now().strftime("%d %b %Y  |  %I:%M:%S %p")
        self.clock_label.configure(text=now)
        self.root.after(1000, self._refresh_clock)

    def _refresh_tasks(self) -> None:
        self.task_list.delete(0, "end")
        for item in self.tasks:
            done = bool(item["done"])
            text = str(item["text"])
            marker = "[x]" if done else "[ ]"
            self.task_list.insert("end", f"{marker} {text}")
        self._refresh_stats()

    def _refresh_stats(self) -> None:
        total = len(self.tasks)
        done = sum(1 for item in self.tasks if bool(item["done"]))
        pending = total - done
        self.total_value.configure(text=str(total))
        self.done_value.configure(text=str(done))
        self.pending_value.configure(text=str(pending))

    def add_task(self) -> None:
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Missing task", "Please enter a task first.")
            return
        self.tasks.append({"text": text, "done": False})
        self.task_entry.delete(0, "end")
        self.selected_index = None
        self._refresh_tasks()

    def on_task_select(self, _: tk.Event) -> None:
        selected = self.task_list.curselection()
        if not selected:
            self.selected_index = None
            return
        self.selected_index = selected[0]
        selected_text = str(self.tasks[self.selected_index]["text"])
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, selected_text)

    def update_task(self) -> None:
        if self.selected_index is None:
            messagebox.showinfo("Select task", "Select a task from the list to update.")
            return
        new_text = self.task_entry.get().strip()
        if not new_text:
            messagebox.showwarning("Missing text", "Task text cannot be empty.")
            return
        self.tasks[self.selected_index]["text"] = new_text
        self._refresh_tasks()

    def toggle_done(self) -> None:
        if self.selected_index is None:
            messagebox.showinfo("Select task", "Select a task to toggle status.")
            return
        current = bool(self.tasks[self.selected_index]["done"])
        self.tasks[self.selected_index]["done"] = not current
        self._refresh_tasks()

    def delete_task(self) -> None:
        if self.selected_index is None:
            messagebox.showinfo("Select task", "Select a task to delete.")
            return
        self.tasks.pop(self.selected_index)
        self.selected_index = None
        self.task_entry.delete(0, "end")
        self._refresh_tasks()

    def clear_all(self) -> None:
        if not self.tasks:
            return
        ok = messagebox.askyesno("Clear all", "Delete all tasks from your board?")
        if not ok:
            return
        self.tasks.clear()
        self.selected_index = None
        self.task_entry.delete(0, "end")
        self._refresh_tasks()


if __name__ == "__main__":
    root_window = tk.Tk()
    app = TodoFrontendApp(root_window)
    root_window.mainloop()
