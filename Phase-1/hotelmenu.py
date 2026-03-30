import tkinter as tk
from tkinter import messagebox
from datetime import datetime


MENU = {
    "Pizza": 40,
    "Pasta": 50,
    "Burger": 60,
    "Salad": 70,
    "Coffee": 80,
}

COLORS = {
    "bg": "#F4F1EA",
    "card": "#FFFDF8",
    "ink": "#2E2A24",
    "muted": "#6E655A",
    "accent": "#0F9D8C",
    "accent_hover": "#0B7F72",
    "danger": "#D64545",
    "danger_hover": "#BA3333",
    "highlight": "#FFB545",
    "line": "#E9E1D5",
}


class RestaurantApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Python Restaurant")
        self.root.geometry("900x620")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        self.order_items = []
        self.total_amount = 0
        self.tax_rate = 0.05
        self.animated_grand_total = 0.0
        self.total_animation_id = None

        self.title_full_text = "PYTHON RESTAURANT"
        self.title_display_text = ""
        self.title_index = 0

        self.selected_item = tk.StringVar(value="Pizza")
        self.quantity_var = tk.StringVar(value="1")

        self._build_ui()
        self._animate_title()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=COLORS["ink"], height=88)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.title_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 24, "bold"),
            fg=COLORS["highlight"],
            bg=COLORS["ink"],
        )
        self.title_label.pack(pady=(16, 2))

        subtitle = tk.Label(
            header,
            text="Fresh picks. Fast billing. Clean vibes.",
            font=("Segoe UI", 10),
            fg="#DCCFB9",
            bg=COLORS["ink"],
        )
        subtitle.pack()

        content = tk.Frame(self.root, bg=COLORS["bg"], padx=16, pady=14)
        content.pack(fill="both", expand=True)

        left_col = tk.Frame(content, bg=COLORS["bg"])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_col = tk.Frame(content, bg=COLORS["bg"])
        right_col.pack(side="right", fill="both", expand=True, padx=(8, 0))

        menu_card = tk.LabelFrame(
            left_col,
            text=" Menu ",
            padx=14,
            pady=10,
            bg=COLORS["card"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10, "bold"),
        )
        menu_card.pack(fill="x", pady=(0, 10))

        for item, price in MENU.items():
            tk.Label(
                menu_card,
                text=f"{item:<10} Rs{price}",
                font=("Consolas", 11),
                fg=COLORS["ink"],
                bg=COLORS["card"],
            ).pack(anchor="w", pady=1)

        order_card = tk.LabelFrame(
            left_col,
            text=" Place Order ",
            padx=14,
            pady=12,
            bg=COLORS["card"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10, "bold"),
        )
        order_card.pack(fill="x", pady=(0, 10))

        tk.Label(
            order_card,
            text="Select item",
            font=("Segoe UI", 10),
            bg=COLORS["card"],
            fg=COLORS["muted"],
        ).grid(row=0, column=0, sticky="w")

        item_menu = tk.OptionMenu(order_card, self.selected_item, *MENU.keys())
        item_menu.config(
            width=16,
            font=("Segoe UI", 10),
            bg="#F8F5EE",
            fg=COLORS["ink"],
            highlightthickness=0,
            bd=0,
        )
        item_menu["menu"].config(
            font=("Segoe UI", 10), bg="white", fg=COLORS["ink"])
        item_menu.grid(row=1, column=0, padx=(0, 10), pady=(2, 8), sticky="w")

        tk.Label(
            order_card,
            text="Quantity",
            font=("Segoe UI", 10),
            bg=COLORS["card"],
            fg=COLORS["muted"],
        ).grid(row=0, column=1, sticky="w")

        qty_entry = tk.Entry(
            order_card,
            textvariable=self.quantity_var,
            width=8,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        qty_entry.grid(row=1, column=1, pady=(2, 8), sticky="w")

        actions_row = tk.Frame(order_card, bg=COLORS["card"])
        actions_row.grid(row=2, column=0, columnspan=2,
                         pady=(4, 0), sticky="w")

        add_button = self._make_button(
            actions_row,
            text="Add Item",
            command=self.add_item,
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_hover"],
        )
        add_button.pack(side="left", padx=(0, 8))

        remove_button = self._make_button(
            actions_row,
            text="Remove Last",
            command=self.remove_last_item,
            bg="#9B7B3F",
            hover_bg="#7F642F",
        )
        remove_button.pack(side="left")

        summary_card = tk.LabelFrame(
            left_col,
            text=" Order Summary ",
            padx=14,
            pady=12,
            bg=COLORS["card"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10, "bold"),
        )
        summary_card.pack(fill="both", expand=True)

        self.order_listbox = tk.Listbox(
            summary_card,
            font=("Consolas", 10),
            height=12,
            bg="#FEFCF7",
            fg=COLORS["ink"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["line"],
            selectbackground="#D5EFEA",
            activestyle="none",
        )
        self.order_listbox.pack(fill="both", expand=True)

        bill_card = tk.LabelFrame(
            right_col,
            text=" Bill Section ",
            padx=14,
            pady=12,
            bg=COLORS["card"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10, "bold"),
        )
        bill_card.pack(fill="both", expand=True)

        self.subtotal_label = tk.Label(
            bill_card,
            text="Subtotal: Rs0.00",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            bg=COLORS["card"],
            fg=COLORS["ink"],
        )
        self.subtotal_label.pack(fill="x")

        self.tax_label = tk.Label(
            bill_card,
            text="Tax (5%): Rs0.00",
            font=("Segoe UI", 11),
            anchor="w",
            bg=COLORS["card"],
            fg=COLORS["muted"],
        )
        self.tax_label.pack(fill="x", pady=(2, 0))

        self.grand_total_label = tk.Label(
            bill_card,
            text="Grand Total: Rs0.00",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            pady=6,
            bg=COLORS["card"],
            fg=COLORS["accent"],
        )
        self.grand_total_label.pack(fill="x")

        self.bill_preview = tk.Text(
            bill_card,
            height=17,
            font=("Consolas", 9),
            state="disabled",
            wrap="word",
            bg="#FFFCF6",
            fg=COLORS["ink"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["line"],
        )
        self.bill_preview.pack(fill="both", expand=True, pady=(6, 8))

        self.total_label = tk.Label(
            bill_card,
            text="Live Total: Rs0",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            bg=COLORS["card"],
            fg=COLORS["ink"],
        )
        self.total_label.pack(fill="x")

        footer_actions = tk.Frame(right_col, bg=COLORS["bg"])
        footer_actions.pack(fill="x", pady=(10, 0))

        checkout_button = self._make_button(
            footer_actions,
            text="Checkout",
            command=self.checkout,
            bg="#2F6FED",
            hover_bg="#2659BD",
            width=14,
        )
        checkout_button.pack(side="left", padx=(0, 8))

        clear_button = self._make_button(
            footer_actions,
            text="Clear Order",
            command=self.clear_order,
            bg=COLORS["danger"],
            hover_bg=COLORS["danger_hover"],
            width=14,
        )
        clear_button.pack(side="left")

        self._update_bill_section()

    def _make_button(self, parent, text, command, bg, hover_bg, width=12):
        btn = tk.Button(
            parent,
            text=text,
            width=width,
            command=command,
            bg=bg,
            fg="white",
            activebackground=hover_bg,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=8,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        btn.bind("<Enter>", lambda _e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
        return btn

    def _animate_title(self) -> None:
        if self.title_index <= len(self.title_full_text):
            self.title_display_text = self.title_full_text[: self.title_index]
            self.title_label.config(text=self.title_display_text)
            self.title_index += 1
            self.root.after(60, self._animate_title)

    def add_item(self) -> None:
        item = self.selected_item.get()
        qty_text = self.quantity_var.get().strip()

        if not qty_text.isdigit() or int(qty_text) <= 0:
            messagebox.showerror("Invalid Quantity",
                                 "Please enter a valid positive quantity.")
            return

        qty = int(qty_text)
        price = MENU[item]
        line_total = qty * price

        self.order_items.append((item, qty, line_total))
        self.total_amount += line_total

        self.order_listbox.insert(
            tk.END,
            f"{item:<10} x {qty:<2} @ Rs{price:<3} = Rs{line_total}",
        )
        self.total_label.config(text=f"Total: Rs{self.total_amount}")
        self._flash_summary()
        self._update_bill_section()
        self.quantity_var.set("1")

    def remove_last_item(self) -> None:
        if not self.order_items:
            messagebox.showinfo("Nothing To Remove", "No items in order list.")
            return

        removed_item, _qty, line_total = self.order_items.pop()
        self.total_amount -= line_total
        self.order_listbox.delete(tk.END)
        self.total_label.config(text=f"Total: Rs{self.total_amount}")
        self._update_bill_section()
        messagebox.showinfo(
            "Removed", f"Removed {removed_item} from your order.")

    def checkout(self) -> None:
        if self.total_amount == 0:
            messagebox.showinfo(
                "No Items", "Please add at least one item to place an order.")
            return

        grand_total = self.total_amount + (self.total_amount * self.tax_rate)
        messagebox.showinfo(
            "Order Confirmed",
            f"Awesome choice!\nYour final bill is Rs{grand_total:.2f}.",
        )

    def clear_order(self) -> None:
        self.order_items.clear()
        self.total_amount = 0
        self.order_listbox.delete(0, tk.END)
        self.total_label.config(text="Live Total: Rs0")
        self._update_bill_section()
        self.quantity_var.set("1")

    def _update_bill_section(self) -> None:
        subtotal = float(self.total_amount)
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax

        self.subtotal_label.config(text=f"Subtotal: Rs{subtotal:.2f}")
        self.tax_label.config(text=f"Tax (5%): Rs{tax:.2f}")
        self._animate_grand_total(grand_total)

        lines = [
            "------ PYTHON RESTAURANT BILL ------",
            f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            "",
        ]

        if self.order_items:
            lines.append("Item       Qty   Total")
            for item, qty, line_total in self.order_items:
                lines.append(f"{item:<10} {qty:<5} Rs{line_total:.2f}")
        else:
            lines.append("No items added yet.")

        lines.extend(
            [
                "",
                f"Subtotal: Rs{subtotal:.2f}",
                f"Tax (5%): Rs{tax:.2f}",
                f"Grand Total: Rs{grand_total:.2f}",
            ]
        )

        self.bill_preview.config(state="normal")
        self.bill_preview.delete("1.0", tk.END)
        self.bill_preview.insert("1.0", "\n".join(lines))
        self.bill_preview.config(state="disabled")

    def _animate_grand_total(self, target_value: float) -> None:
        if self.total_animation_id:
            self.root.after_cancel(self.total_animation_id)
            self.total_animation_id = None

        self._animate_value_step(target_value)

    def _animate_value_step(self, target_value: float) -> None:
        diff = target_value - self.animated_grand_total

        if abs(diff) < 0.05:
            self.animated_grand_total = target_value
            self.grand_total_label.config(
                text=f"Grand Total: Rs{self.animated_grand_total:.2f}"
            )
            return

        self.animated_grand_total += diff * 0.25
        self.grand_total_label.config(
            text=f"Grand Total: Rs{self.animated_grand_total:.2f}"
        )
        self.total_animation_id = self.root.after(
            18, lambda: self._animate_value_step(target_value)
        )

    def _flash_summary(self) -> None:
        self.order_listbox.config(highlightbackground=COLORS["highlight"])
        self.root.after(
            180,
            lambda: self.order_listbox.config(
                highlightbackground=COLORS["line"]),
        )


if __name__ == "__main__":
    app_root = tk.Tk()
    app = RestaurantApp(app_root)
    app_root.mainloop()
