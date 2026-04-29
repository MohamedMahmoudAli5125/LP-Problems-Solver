import customtkinter as ctk

_GREEN  = "#4ade80"
_YELLOW = "#facc15"
_BLUE   = "#60a5fa"
_RED    = "#f87171"
_PURPLE = "#c084fc"
_GRAY   = "#94a3b8"
_BG     = "#0f172a"
_PANEL  = "#1e293b"
_BORDER = "#334155"


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=_BG, corner_radius=10, **kwargs)
        self._build_empty()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _build_empty(self):
        self._clear()
        ctk.CTkLabel(self, text="No solution yet", text_color=_GRAY,
                     font=("Courier New", 11)).pack(pady=8)

    def show(self, status: str, solution: dict):
        self._clear()

        color = _GREEN if status == "Optimal" else (_YELLOW if status == "Unbounded" else _RED)
        bar = ctk.CTkFrame(self, fg_color=color, corner_radius=6, height=26)
        bar.pack(fill="x", padx=10, pady=(8, 4))
        bar.pack_propagate(False)
        ctk.CTkLabel(bar, text=f"● {status.upper()}",
                     font=("Courier New", 11, "bold"), text_color=_BG).pack(expand=True)

        if status != "Optimal" or not solution:
            return

        obj_val = solution.get("objective_value", "N/A")
        obj_str = f"{obj_val:.6g}" if isinstance(obj_val, float) else str(obj_val)

        mid = ctk.CTkFrame(self, fg_color=_PANEL, corner_radius=8)
        mid.pack(fill="x", padx=10, pady=(0, 8))

        obj_row = ctk.CTkFrame(mid, fg_color="transparent")
        obj_row.pack(fill="x", padx=10, pady=(6, 4))
        ctk.CTkLabel(obj_row, text="Z =", font=("Courier New", 11),
                     text_color=_GRAY).pack(side="left")
        ctk.CTkLabel(obj_row, text=f"  {obj_str}",
                     font=("Courier New", 16, "bold"), text_color=_YELLOW).pack(side="left")

        ctk.CTkFrame(mid, fg_color=_BORDER, height=1).pack(fill="x", padx=8)

        group_color = {"x": _BLUE, "s": _GREEN, "a": _RED}
        vars_only = {k: v for k, v in solution.items() if k != "objective_value"}
        var_list = list(vars_only.items())

        for i, (name, val) in enumerate(var_list):
            first_char = name.lstrip()[0] if name.strip() else "?"
            pill_color = group_color.get(first_char, _PURPLE)
            is_zero = abs(float(val)) < 1e-9
            val_str = f"{float(val):.6g}"

            row = ctk.CTkFrame(mid, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)

            pill = ctk.CTkFrame(row, fg_color=pill_color, corner_radius=5, width=46, height=20)
            pill.pack(side="left", padx=(0, 8))
            pill.pack_propagate(False)
            ctk.CTkLabel(pill, text=name, font=("Courier New", 10, "bold"),
                         text_color=_BG).pack(expand=True)

            ctk.CTkLabel(row, text=f"= {val_str}",
                         font=("Courier New", 11, "bold"),
                         text_color=_GRAY if is_zero else pill_color).pack(side="left")

            if i < len(var_list) - 1:
                ctk.CTkFrame(mid, fg_color=_BORDER, height=1).pack(fill="x", padx=10)

        ctk.CTkFrame(mid, fg_color="transparent", height=4).pack()


class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text="Result", font=("Courier New", 12, "bold"),
                     anchor="w", text_color=_GRAY).pack(fill="x", padx=10, pady=(8, 2))

        self.card_container = ctk.CTkScrollableFrame(self, height=220, fg_color="transparent")
        self.card_container.pack(fill="x", padx=6, pady=(0, 4))

        self.result_card = ResultCard(self.card_container)
        self.result_card.pack(fill="x")

        ctk.CTkFrame(self, fg_color=_BORDER, height=1).pack(fill="x", padx=10, pady=3)

        ctk.CTkLabel(self, text="Simplex Trace", font=("Courier New", 12, "bold"),
                     anchor="w", text_color=_GRAY).pack(fill="x", padx=10, pady=(2, 2))

        self.trace_box = ctk.CTkTextbox(
            self, font=("Courier New", 11), wrap="none",
            state="disabled", fg_color=_BG, text_color="#cbd5e1",
        )
        self.trace_box.pack(fill="both", expand=True, padx=6, pady=(0, 8))

    def display_result(self, trace: str, status: str, solution: dict):
        self.result_card.show(status, solution)

        self.trace_box.configure(state="normal")
        self.trace_box.delete("1.0", "end")
        self.trace_box.insert("end", trace)
        self.trace_box.configure(state="disabled")
        self.trace_box.yview_moveto(0.0)