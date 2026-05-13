# ============================================================
#  ui/sidebar.py — Sidebar navigasi + parameter global
# ============================================================

import tkinter as tk
from config import *


class Sidebar(tk.Frame):
    def __init__(self, master, on_navigate, on_param_change):
        super().__init__(master, bg=C_PANEL, width=220)
        self.pack_propagate(False)
        self._on_navigate    = on_navigate
        self._on_param_change = on_param_change
        self._nav_refs = {}
        self._active   = None

        self._build_nav()
        self._build_params()

    # ── Navigasi ─────────────────────────────────────────────
    def _build_nav(self):
        tk.Label(self, text="NAVIGASI", bg=C_PANEL, fg=C_TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(
                 anchor="w", padx=16, pady=(16, 8))

        nav_items = [
            ("🏠", "Dashboard",  "dashboard"),
            ("🔢", "Kalkulator", "calculator"),
            ("📈", "Grafik",     "chart"),
            ("📋", "Tabel Data", "table"),
            ("ℹ️", "Tentang",    "about"),
        ]
        for icon, label, tab in nav_items:
            self._make_nav_btn(icon, label, tab)

    def _make_nav_btn(self, icon, label, tab):
        fr = tk.Frame(self, bg=C_PANEL, cursor="hand2")
        fr.pack(fill="x", padx=8, pady=2)
        tk.Label(fr, text=icon, bg=C_PANEL, fg=C_TEXT,
                 font=("Segoe UI", 12), width=3).pack(
                 side="left", padx=(8, 4), pady=8)
        lbl = tk.Label(fr, text=label, bg=C_PANEL, fg=C_TEXT,
                        font=("Segoe UI", 10), anchor="w")
        lbl.pack(side="left", fill="x", expand=True)
        ind = tk.Frame(fr, bg=C_PANEL, width=3)
        ind.pack(side="right", fill="y")

        def click(e=None, t=tab):
            self._on_navigate(t)
            self._set_active(t)

        for w in (fr, lbl):
            w.bind("<Button-1>", click)
            w.bind("<Enter>",
                   lambda e, f=fr: f.config(bg=C_HOVER))
            w.bind("<Leave>",
                   lambda e, f=fr, t=tab:
                   f.config(bg=C_HOVER if self._active == t else C_PANEL))

        self._nav_refs[tab] = (fr, lbl, ind)

    def _set_active(self, tab):
        for t, (fr, lbl, ind) in self._nav_refs.items():
            active = (t == tab)
            fr.config( bg=C_HOVER if active else C_PANEL)
            lbl.config(fg=C_ACCENT if active else C_TEXT)
            ind.config(bg=C_ACCENT if active else C_PANEL)
        self._active = tab

    def activate(self, tab):
        self._set_active(tab)

    # ── Parameter global ─────────────────────────────────────
    def _build_params(self):
        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x", padx=16, pady=20)
        tk.Label(self, text="PARAMETER GLOBAL", bg=C_PANEL, fg=C_TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(
                 anchor="w", padx=16, pady=(0, 8))

        params = [
            ("Jarak Harian (km)", "dist_var",  "30"),
            ("Harga BBM (Rp/L)",  "price_var", "10000"),
            ("Kecepatan (km/h)",  "speed_var", "50"),
        ]
        for label, varname, default in params:
            tk.Label(self, text=label, bg=C_PANEL, fg=C_TEXT_DIM,
                     font=("Segoe UI", 8)).pack(anchor="w", padx=16, pady=(6, 2))
            var = tk.StringVar(value=default)
            setattr(self, varname, var)
            e = tk.Entry(self, textvariable=var, bg=C_CARD, fg=C_ACCENT,
                         insertbackground=C_ACCENT,
                         font=("Segoe UI", 10, "bold"),
                         relief="flat", bd=0, highlightthickness=1,
                         highlightbackground=C_BORDER,
                         highlightcolor=C_ACCENT, width=16)
            e.pack(padx=16, pady=(0, 2), ipady=4)
            var.trace_add("write", lambda *a: self._on_param_change())

    def get_params(self):
        """Kembalikan (dist, price, speed) sebagai float."""
        return (
            float(self.dist_var.get()),
            float(self.price_var.get()),
            float(self.speed_var.get()),
        )
