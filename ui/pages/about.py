# ============================================================
#  ui/pages/about.py — Halaman Tentang / Info Proyek
# ============================================================

import tkinter as tk
from tkinter import ttk

from config import *


class AboutPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C_BG)
        self._build()

    def _build(self):
        # Scrollable canvas
        canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=C_BG)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._title_card(inner)
        self._team_card(inner)
        self._method_card(inner)
        self._stack_card(inner)

    def _card(self, parent, title, color):
        f = tk.Frame(parent, bg=C_CARD, padx=24, pady=16)
        f.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(f, text=title, bg=C_CARD, fg=color,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        return f

    def _title_card(self, parent):
        f = tk.Frame(parent, bg=C_CARD, padx=32, pady=24)
        f.pack(fill="x", padx=16, pady=(16, 12))
        tk.Label(f, text="⛽  FUEL ESTIMATOR", bg=C_CARD, fg=C_ACCENT,
                 font=("Segoe UI", 20, "bold")).pack()
        tk.Label(f, text="Analisis Estimasi Pengeluaran Bahan Bakar Kendaraan Harian",
                 bg=C_CARD, fg=C_TEXT, font=("Segoe UI", 12)).pack(pady=(4, 0))
        tk.Label(f, text="Menggunakan Metode Numerik Deret Taylor",
                 bg=C_CARD, fg=C_TEXT_DIM, font=("Segoe UI", 10)).pack()
        tk.Frame(f, bg=C_ACCENT, height=2).pack(fill="x", pady=16)
        tk.Label(f, text="PROGRAM STUDI INFORMATIKA  •  FAKULTAS TEKNIK  •  UNIVERSITAS SILIWANGI  •  2026",
                 bg=C_CARD, fg=C_TEXT_DIM, font=("Segoe UI", 9)).pack()

    def _team_card(self, parent):
        f = self._card(parent, "Tim Peneliti", C_ACCENT2)
        for name, nim in TEAM_MEMBERS:
            row = tk.Frame(f, bg=C_CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text="▸", bg=C_CARD, fg=C_ACCENT,
                     font=("Segoe UI", 10)).pack(side="left", padx=(0, 8))
            tk.Label(row, text=name, bg=C_CARD, fg=C_TEXT,
                     font=("Segoe UI", 10, "bold"), width=28, anchor="w").pack(side="left")
            tk.Label(row, text=nim, bg=C_CARD, fg=C_TEXT_DIM,
                     font=("Segoe UI", 9)).pack(side="left")

    def _method_card(self, parent):
        f = self._card(parent, "Metode yang Digunakan", C_ACCENT3)
        formulas = [
            ("Deret Taylor Orde-1", "C(v) ≈ C(v₀) + C'(v₀)(v − v₀)"),
            ("Model Linear",        "C(v) = av + b"),
            ("Titik Ekspansi",      "v₀ = 50 km/jam"),
            ("Volume BBM",          "V = C(v) × Jarak (km)"),
            ("Biaya Harian",        "B = V × Harga (Rp/L)"),
        ]
        for title, formula in formulas:
            row = tk.Frame(f, bg=C_CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=title + ":", bg=C_CARD, fg=C_TEXT_DIM,
                font=("Segoe UI", 9), width=20, anchor="w").pack(side="left")
            tk.Label(row, text=formula, bg=C_BG, fg=C_ACCENT,
                font=("Courier New", 9), padx=8, pady=2).pack(side="left")
    
    def _stack_card(self, parent):
        f = self._card(parent, "Tech Stack", C_ACCENT4)
        stack = [
            ("Python ",   "Bahasa Pemrograman"),
            ("Tkinter",       "GUI Framework"),
            ("Matplotlib",    "Visualisasi Grafik"),
            ("NumPy",         "Komputasi Numerik"),
        ]
        for tech, desc in stack:
            row = tk.Frame(f, bg=C_CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"  {tech}", bg=C_CARD, fg=C_ACCENT2,
                font=("Segoe UI", 9, "bold"), width=18, anchor="w").pack(side="left")
            tk.Label(row, text=desc, bg=C_CARD, fg=C_TEXT_DIM,
                font=("Segoe UI", 9)).pack(side="left")
