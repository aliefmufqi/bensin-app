# ============================================================
#  ui/pages/calculator.py — Halaman Kalkulator Interaktif
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

from config import *
from core.model import FuelModel
from ui.widgets import GlowButton


class CalculatorPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C_BG)
        self._vars  = {}   # input StringVar
        self._cards = {}   # result label refs
        self._build()
        self._run()

    # ── Build layout ─────────────────────────────────────────
    def _build(self):
        tk.Label(self, text="Kalkulator Interaktif", bg=C_BG, fg=C_TEXT,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(16, 4))
        tk.Label(self, text="Hitung estimasi pengeluaran BBM dengan parameter kustom",
                 bg=C_BG, fg=C_TEXT_DIM, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 12))

        cols = tk.Frame(self, bg=C_BG)
        cols.pack(fill="both", expand=True)
        self._build_input(cols)
        self._build_output(cols)

    # ── Input form (kiri) ────────────────────────────────────
    def _build_input(self, parent):
        frame = tk.Frame(parent, bg=C_CARD, width=380)
        frame.pack(side="left", fill="y", padx=(0, 12))
        frame.pack_propagate(False)

        tk.Label(frame, text="  Input Parameter", bg=C_CARD, fg=C_ACCENT,
                 font=("Segoe UI", 11, "bold"), pady=12).pack(anchor="w")

        sections = {
            "Motor 110cc": [
                ("Efisiensi @50 km/h (km/L)", "eff_110_50", "50"),
                ("Efisiensi @60 km/h (km/L)", "eff_110_60", "45"),
            ],
            "Motor 125cc": [
                ("Efisiensi @50 km/h (km/L)", "eff_125_50", "45"),
                ("Efisiensi @60 km/h (km/L)", "eff_125_60", "40"),
            ],
            "Motor 150cc": [
                ("Efisiensi @50 km/h (km/L)", "eff_150_50", "40"),
                ("Efisiensi @60 km/h (km/L)", "eff_150_60", "35"),
            ],
            "Kondisi Berkendara": [
                ("Kecepatan (km/h)",  "speed", "50"),
                ("Jarak Harian (km)", "dist",  "30"),
                ("Harga BBM (Rp/L)",  "price", "10000"),
            ],
        }
        for sec_title, fields in sections.items():
            sec = tk.Frame(frame, bg=C_CARD)
            sec.pack(fill="x", padx=12, pady=(8, 0))
            tk.Label(sec, text=sec_title, bg=C_CARD, fg=C_ACCENT2,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
            for label, key, default in fields:
                row = tk.Frame(sec, bg=C_CARD)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=label, bg=C_CARD, fg=C_TEXT_DIM,
                         font=("Segoe UI", 8), width=26, anchor="w").pack(side="left")
                var = tk.StringVar(value=default)
                self._vars[key] = var
                tk.Entry(row, textvariable=var, bg=C_BG, fg=C_ACCENT,
                         insertbackground=C_ACCENT, font=("Segoe UI", 9, "bold"),
                         relief="flat", bd=0, highlightthickness=1,
                         highlightbackground=C_BORDER,
                         highlightcolor=C_ACCENT, width=10).pack(
                         side="right", ipady=3)

        btn_row = tk.Frame(frame, bg=C_CARD)
        btn_row.pack(padx=12, pady=16, fill="x")
        GlowButton(btn_row, "▶  HITUNG", self._run,
                   color=C_ACCENT2, width=160, height=38).pack(side="left")
        GlowButton(btn_row, "↺  RESET", self._reset,
                   color=C_TEXT_DIM, width=100, height=38).pack(side="left", padx=(8, 0))

    # ── Output panel (kanan) ─────────────────────────────────
    def _build_output(self, parent):
        right = tk.Frame(parent, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        # Result cards (3 motor)
        cards_row = tk.Frame(right, bg=C_BG)
        cards_row.pack(fill="x", pady=(0, 12))
        for cc in ["110cc", "125cc", "150cc"]:
            col = MOTOR_COLORS[cc]
            card = tk.Frame(cards_row, bg=C_CARD, padx=16, pady=12)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(card, text=f"● Motor {cc}", bg=C_CARD, fg=col,
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Frame(card, bg=col, height=2).pack(fill="x", pady=(6, 8))

            info = {}
            rows = [("Konsumsi",      "l/km"),
                    ("Volume BBM",    "liter/hari"),
                    ("Biaya Harian",  "Rp"),
                    ("Biaya Bulanan", "Rp"),
                    ("Gradien (a)",   ""),
                    ("Konstanta (b)", "")]
            for rname, runit in rows:
                rr = tk.Frame(card, bg=C_CARD)
                rr.pack(fill="x", pady=1)
                tk.Label(rr, text=rname, bg=C_CARD, fg=C_TEXT_DIM,
                         font=("Segoe UI", 8), width=14, anchor="w").pack(side="left")
                vl = tk.Label(rr, text="—", bg=C_CARD, fg=C_TEXT,
                              font=("Segoe UI", 9, "bold"), anchor="e")
                vl.pack(side="right")
                if runit:
                    tk.Label(rr, text=runit, bg=C_CARD, fg=C_TEXT_DIM,
                             font=("Segoe UI", 7)).pack(side="right", padx=(0, 4))
                info[rname] = vl
            self._cards[cc] = info

        # Sensitivity table
        sens = tk.Frame(right, bg=C_CARD)
        sens.pack(fill="both", expand=True)
        tk.Label(sens, text="  Analisis Sensitivitas Harga BBM", bg=C_CARD,
                 fg=C_ACCENT, font=("Segoe UI", 10, "bold"), pady=8).pack(anchor="w")
        cols = ["Skenario", "Harga (Rp/L)", "110cc (Rp)", "125cc (Rp)", "150cc (Rp)"]
        self._sens_tree = ttk.Treeview(sens, columns=cols, show="headings", height=5)
        for col in cols:
            self._sens_tree.heading(col, text=col)
            self._sens_tree.column(col, width=130, anchor="center")
        self._sens_tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # ── Hitung ───────────────────────────────────────────────
    def _run(self):
        try:
            models = {}
            for cc_num in ["110", "125", "150"]:
                cc  = f"{cc_num}cc"
                e1  = float(self._vars[f"eff_{cc_num}_50"].get())
                e2  = float(self._vars[f"eff_{cc_num}_60"].get())
                models[cc] = FuelModel(cc, e1, e2)
            speed = float(self._vars["speed"].get())
            dist  = float(self._vars["dist"].get())
            price = float(self._vars["price"].get())
        except Exception as ex:
            messagebox.showerror("Input Error", f"Periksa nilai input:\n{ex}")
            return

        for cc, m in models.items():
            vol, cost = m.daily_cost(speed, dist, price)
            info = self._cards[cc]
            info["Konsumsi"].config(     text=f"{m.taylor(speed):.5f}")
            info["Volume BBM"].config(   text=f"{vol:.4f}")
            info["Biaya Harian"].config( text=f"{cost:,.0f}")
            info["Biaya Bulanan"].config(text=f"{cost*25:,.0f}")
            info["Gradien (a)"].config(  text=f"{m.a:.6f}")
            info["Konstanta (b)"].config(text=f"{m.b:.5f}")

        # Sensitivity table
        for row in self._sens_tree.get_children():
            self._sens_tree.delete(row)
        scenarios = [
            ("Harga Saat Ini", 0),
            ("Naik 10%",      0.10),
            ("Naik 20%",      0.20),
            ("Naik 30%",      0.30),
            ("Naik 50%",      0.50),
        ]
        for label, pct in scenarios:
            p   = price * (1 + pct)
            row = [label, f"Rp {p:,.0f}"]
            for cc, m in models.items():
                _, c = m.daily_cost(speed, dist, p)
                row.append(f"Rp {c:,.0f}")
            self._sens_tree.insert("", "end", values=row)

    # ── Reset ────────────────────────────────────────────────
    def _reset(self):
        defaults = {
            "eff_110_50": "50", "eff_110_60": "45",
            "eff_125_50": "45", "eff_125_60": "40",
            "eff_150_50": "40", "eff_150_60": "35",
            "speed": "50", "dist": "30", "price": "10000",
        }
        for k, v in defaults.items():
            self._vars[k].set(v)
        self._run()
