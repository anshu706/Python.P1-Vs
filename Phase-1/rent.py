import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont


COLORS = {
    "bg": "#F8F6F3",
    "card": "#FFFFFF",
    "card_light": "#FAFBFC",
    "ink": "#1A1A1A",
    "text": "#333333",
    "muted": "#757575",
    "accent": "#00C896",
    "accent_hover": "#00A876",
    "accent_light": "#E6F9F2",
    "highlight": "#FF9800",
    "line": "#E8E8E8",
    "success": "#4CAF50",
    "border": "#E0E0E0",
    "shadow": "#00000015",
}


class RentShareApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Flat Expense Splitter")
        self.root.geometry("1000x690")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        self.rent_var = tk.StringVar(value="0")
        self.food_var = tk.StringVar(value="0")
        self.electricity_units_var = tk.StringVar(value="0")
        self.charge_per_unit_var = tk.StringVar(value="0")
        self.persons_var = tk.StringVar(value="0")

        self.total_electricity = 0
        self.total_bill = 0
        self.per_person_cost = 0

        self._build_ui()
        self._update_calculation()

    def _build_ui(self) -> None:
        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=COLORS["ink"], height=86)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_font = tkFont.Font(family="Segoe UI", size=24, weight="bold")
        title = tk.Label(
            header,
            text="💰 Flat Expense Splitter",
            font=title_font,
            fg=COLORS["accent"],
            bg=COLORS["ink"],
        )
        title.pack(pady=(10, 2))

        subtitle = tk.Label(
            header,
            text="Split rent, food & utilities fairly among flatmates",
            font=("Segoe UI", 10),
            fg="#A0A0A0",
            bg=COLORS["ink"],
        )
        subtitle.pack()

    def _build_content(self) -> None:
        main_container = tk.Frame(self.root, bg=COLORS["bg"])
        main_container.pack(fill="both", expand=True, padx=14, pady=10)

        left_panel = tk.Frame(main_container, bg=COLORS["bg"])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_panel = tk.Frame(main_container, bg=COLORS["bg"])
        right_panel.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self._build_input_section(left_panel)
        self._build_results_section(right_panel)

        button_bar = tk.Frame(self.root, bg=COLORS["bg"])
        button_bar.pack(fill="x", padx=14, pady=(0, 10))

        self._make_button(button_bar, "↻ Reset", self._reset_form,
                          COLORS["muted"], "#5A5A5A", 12).pack(side="left", padx=(0, 10))
        self._make_button(button_bar, "📋 Copy Summary", self._copy_summary,
                          COLORS["accent"], COLORS["accent_hover"], 12).pack(side="left")

    def _build_input_section(self, parent) -> None:
        title_frame = tk.Frame(parent, bg=COLORS["bg"])
        title_frame.pack(fill="x", pady=(0, 8))

        input_title = tk.Label(
            title_frame,
            text="📝 Expense Details",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["bg"],
        )
        input_title.pack(anchor="w")

        input_card = self._make_card(parent)
        input_card.pack(fill="both", padx=1, pady=1)

        self._create_input_field(input_card, "Flat Rent", self.rent_var, "₹")
        self._create_input_field(
            input_card, "Food & Groceries", self.food_var, "₹")
        self._create_input_field(
            input_card, "Electricity Units", self.electricity_units_var, "units")
        self._create_input_field(
            input_card, "Rate per Unit", self.charge_per_unit_var, "₹")
        self._create_input_field(
            input_card, "Number of People", self.persons_var, "people")

        for var in [self.rent_var, self.food_var, self.electricity_units_var, self.charge_per_unit_var, self.persons_var]:
            var.trace_add("write", lambda *_args: self._update_calculation())

    def _build_results_section(self, parent) -> None:
        title_frame = tk.Frame(parent, bg=COLORS["bg"])
        title_frame.pack(fill="x", pady=(0, 8))

        results_title = tk.Label(
            title_frame,
            text="📊 Bill Breakdown",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["bg"],
        )
        results_title.pack(anchor="w")

        results_card = self._make_card(parent)
        results_card.pack(fill="both", expand=False, padx=1, pady=1)

        breakdown_frame = tk.Frame(results_card, bg=COLORS["card"])
        breakdown_frame.pack(fill="x", padx=10, pady=8)

        self.rent_display = self._make_breakdown_item(
            breakdown_frame, "Rent", "Rs 0.00", 0, is_bold=True)
        self.food_display = self._make_breakdown_item(
            breakdown_frame, "Food & Groceries", "Rs 0.00", 1)
        self.electricity_display = self._make_breakdown_item(
            breakdown_frame, "Electricity", "Rs 0.00", 2)

        tk.Frame(breakdown_frame, bg=COLORS["border"], height=1).pack(
            fill="x", pady=10)

        self.total_bill_display = self._make_breakdown_item(
            breakdown_frame, "Total Expenses", "Rs 0.00", 3, is_bold=True, color=COLORS["accent"])

        tk.Frame(breakdown_frame, bg=COLORS["border"], height=1).pack(
            fill="x", pady=10)

        per_person_frame = tk.Frame(breakdown_frame, bg=COLORS["accent_light"])
        per_person_frame.pack(fill="x", padx=0, pady=(6, 0))

        tk.Label(
            per_person_frame,
            text="Per Person Share",
            font=("Segoe UI", 9),
            fg=COLORS["muted"],
            bg=COLORS["accent_light"],
        ).pack(anchor="w", padx=10, pady=(6, 1))

        self.per_person_display = tk.Label(
            per_person_frame,
            text="Rs 0.00",
            font=("Segoe UI", 16, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["accent_light"],
        )
        self.per_person_display.pack(anchor="w", padx=10, pady=(1, 6))

        summary_title = tk.Label(
            parent,
            text="📄 Receipt Summary",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["bg"],
        )
        summary_title.pack(anchor="w", pady=(10, 6))

        summary_card = self._make_card(parent)
        summary_card.pack(fill="both", expand=True, padx=1, pady=1)

        self.summary_text = tk.Text(
            summary_card,
            height=9,
            font=("Courier New", 9),
            bg=COLORS["card_light"],
            fg=COLORS["ink"],
            bd=0,
            relief="flat",
            padx=14,
            pady=12,
            wrap="word",
            state="disabled",
        )
        self.summary_text.pack(fill="both", expand=True)

    def _make_card(self, parent) -> tk.Frame:
        card = tk.Frame(parent, bg=COLORS["card"], relief="flat", bd=0)
        return card

    def _create_input_field(self, parent, label, var, unit) -> None:
        field_frame = tk.Frame(parent, bg=COLORS["card"])
        field_frame.pack(fill="x", padx=10, pady=7)

        label_frame = tk.Frame(field_frame, bg=COLORS["card"])
        label_frame.pack(fill="x", pady=(0, 4))

        tk.Label(
            label_frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["text"],
            bg=COLORS["card"],
        ).pack(side="left")

        tk.Label(
            label_frame,
            text=unit,
            font=("Segoe UI", 9),
            fg=COLORS["muted"],
            bg=COLORS["card"],
        ).pack(side="right")

        entry = tk.Entry(
            field_frame,
            textvariable=var,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=30,
        )
        entry.config(highlightcolor=COLORS["accent"])
        entry.pack(fill="x", ipady=4)
        entry.bind("<FocusIn>", lambda e: entry.config(relief="solid", bd=2))
        entry.bind("<FocusOut>", lambda e: entry.config(relief="solid", bd=1))

    def _make_breakdown_item(self, parent, label, value, row, is_bold=False, color=None) -> tk.Label:
        item_frame = tk.Frame(parent, bg=COLORS["card"])
        item_frame.pack(fill="x", pady=3)

        tk.Label(
            item_frame,
            text=label,
            font=("Segoe UI", 10, "bold" if is_bold else "normal"),
            fg=color if color else COLORS["text"],
            bg=COLORS["card"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        value_label = tk.Label(
            item_frame,
            text=value,
            font=("Segoe UI", 11, "bold" if is_bold else "normal"),
            fg=color if color else COLORS["text"],
            bg=COLORS["card"],
            anchor="e",
        )
        value_label.pack(side="right")

        return value_label

    def _update_calculation(self) -> None:
        try:
            rent = float(self.rent_var.get() or 0)
            food = float(self.food_var.get() or 0)
            electricity_units = float(self.electricity_units_var.get() or 0)
            charge_per_unit = float(self.charge_per_unit_var.get() or 0)
            persons = float(self.persons_var.get() or 1)

            self.total_electricity = electricity_units * charge_per_unit
            self.total_bill = rent + food + self.total_electricity
            self.per_person_cost = self.total_bill / persons if persons > 0 else 0

            self.rent_display.config(text=f"Rs {rent:,.2f}")
            self.food_display.config(text=f"Rs {food:,.2f}")
            self.electricity_display.config(
                text=f"Rs {self.total_electricity:,.2f}")
            self.total_bill_display.config(text=f"Rs {self.total_bill:,.2f}")
            self.per_person_display.config(
                text=f"Rs {self.per_person_cost:,.2f}")

            self._update_summary(
                rent, food, electricity_units, charge_per_unit, persons)

        except ValueError:
            pass

    def _update_summary(self, rent, food, units, charge, persons):
        lines = [
            "┌─────────────────────────────────────┐",
            "│     FLAT EXPENSE RECEIPT            │",
            "└─────────────────────────────────────┘",
            "",
            f"  Rent Amount              ₹ {rent:>10,.2f}",
            f"  Food & Groceries         ₹ {food:>10,.2f}",
            f"  Electricity              ₹ {self.total_electricity:>10,.2f}",
            f"    ({units} units × ₹{charge}/unit)",
            "",
            "  ─────────────────────────────────",
            f"  Total Amount             ₹ {self.total_bill:>10,.2f}",
            "  ─────────────────────────────────",
            "",
            f"  Number of People         {int(persons):>13}",
            f"  Amount Per Person        ₹ {self.per_person_cost:>10,.2f}",
            "",
            "┌─────────────────────────────────────┐",
        ]

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", "\n".join(lines))
        self.summary_text.config(state="disabled")

    def _reset_form(self) -> None:
        self.rent_var.set("0")
        self.food_var.set("0")
        self.electricity_units_var.set("0")
        self.charge_per_unit_var.set("0")
        self.persons_var.set("0")
        self._update_calculation()

    def _copy_summary(self) -> None:
        summary_content = self.summary_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(summary_content)
        messagebox.showinfo("✓ Copied", "Receipt summary copied to clipboard!")

    def _make_button(self, parent, text, command, bg, hover_bg, width=12):
        btn = tk.Button(
            parent,
            text=text,
            width=width,
            command=command,
            bg=bg,
            fg="white" if bg != COLORS["muted"] else "white",
            activebackground=hover_bg,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=7,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            highlightthickness=0,
        )
        btn.bind("<Enter>", lambda _e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
        return btn


if __name__ == "__main__":
    app_root = tk.Tk()
    app = RentShareApp(app_root)
    app_root.mainloop()
