# ============================================================
#  ui/pages/dashboard.py — Halaman Dashboard
# ============================================================

import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import *
from ui.widgets import MetricCard


class DashboardPage(tk.Frame):
    def __init__(self, master, get_models, get_params):
        super().__init__(master, bg=C_BG)
        self.get_models = get_models   # callable → dict[cc, FuelModel]
        self.get_params = get_params   # callable → (dist, price, speed)

        self._build()

    # ── Build layout ─────────────────────────────────────────
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=C_BG)
        hdr.pack(fill="x", pady=(16, 8))
        tk.Label(hdr, text="Dashboard Analisis", bg=C_BG, fg=C_TEXT,
                 font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Label(hdr, text="  Ringkasan estimasi pengeluaran bahan bakar harian",
                 bg=C_BG, fg=C_TEXT_DIM, font=("Segoe UI", 10)).pack(
                 side="left", pady=(6, 0))

        # Metric cards
        card_row = tk.Frame(self, bg=C_BG)
        card_row.pack(fill="x", pady=(0, 16))

        metric_defs = [
            ("110cc Harian",  "Rp 0", "IDR", C_ACCENT),
            ("125cc Harian",  "Rp 0", "IDR", C_ACCENT2),
            ("150cc Harian",  "Rp 0", "IDR", C_ACCENT3),
            ("Selisih Maks",  "Rp 0", "IDR", C_ACCENT4),
            ("Error Taylor",  "0.0000", "l/km", C_SUCCESS),
        ]
        self.cards = {}
        for title, val, unit, color in metric_defs:
            card = MetricCard(card_row, title, val, unit, color)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            self.cards[title] = card

        # Two-column body
        body = tk.Frame(self, bg=C_BG)
        body.pack(fill="both", expand=True)
        self._build_chart_panel(body)
        self._build_info_panel(body)

    def _build_chart_panel(self, parent):
        frame = tk.Frame(parent, bg=C_CARD)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(frame, text="  Konsumsi vs Kecepatan", bg=C_CARD, fg=C_TEXT,
                 font=("Segoe UI", 11, "bold"), pady=10).pack(anchor="w")

        self._fig = Figure(figsize=(6, 4), dpi=96, facecolor=C_CHART_BG)
        self._ax  = self._fig.add_subplot(111, facecolor=C_CHART_BG)
        self._canvas = FigureCanvasTkAgg(self._fig, frame)
        self._canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _build_info_panel(self, parent):
        frame = tk.Frame(parent, bg=C_BG, width=360)
        frame.pack(side="left", fill="y")
        frame.pack_propagate(False)

        # Formula box
        fbox = tk.Frame(frame, bg=C_CARD)
        fbox.pack(fill="x", pady=(0, 10))
        tk.Label(fbox, text="  Formula Deret Taylor Orde-1", bg=C_CARD,
                 fg=C_ACCENT, font=("Segoe UI", 10, "bold"), pady=8).pack(anchor="w")
        formula = (
            "C(v) ≈ C(v₀) + C'(v₀)(v − v₀)\n\n"
            "di mana:\n"
            "  C(v)   = Konsumsi (l/km)\n"
            "  v₀     = Titik pusat (50 km/jam)\n"
            "  C'(v₀) = Gradien (a) = konstan\n\n"
            "Model Linear:\n"
            "  C(v) = av + b\n\n"
            "Volume BBM = C(v) × Jarak (km)\n"
            "Biaya = Volume × Harga (Rp/L)"
        )
        tk.Label(fbox, text=formula, bg=C_CARD, fg=C_TEXT,
                 font=("Courier New", 9), justify="left",
                 padx=12, pady=8).pack(anchor="w")

        # Parameter model
        pbox = tk.Frame(frame, bg=C_CARD)
        pbox.pack(fill="x")
        tk.Label(pbox, text="  Parameter Model", bg=C_CARD, fg=C_ACCENT2,
                 font=("Segoe UI", 10, "bold"), pady=8).pack(anchor="w")

        self._param_labels = {}
        for cc in ["110cc", "125cc", "150cc"]:
            row = tk.Frame(pbox, bg=C_CARD)
            row.pack(fill="x", padx=12, pady=4)
            col = MOTOR_COLORS[cc]
            tk.Label(row, text=f"● {cc}", bg=C_CARD, fg=col,
                     font=("Segoe UI", 9, "bold"), width=7).pack(side="left")
            lbl = tk.Label(row, text="—", bg=C_CARD, fg=C_TEXT,
                           font=("Courier New", 8))
            lbl.pack(side="left")
            self._param_labels[cc] = lbl

    # ── Refresh (dipanggil dari luar saat param berubah) ─────
    def refresh(self):
        try:
            dist, price, speed = self.get_params()
            models = self.get_models()
        except Exception:
            return

        # Update metric cards
        costs = {}
        for cc, m in models.items():
            _, cost = m.daily_cost(speed, dist, price)
            costs[cc] = cost

        for cc in ["110cc", "125cc", "150cc"]:
            key = f"{cc} Harian"
            if key in self.cards:
                self.cards[key].update_value(f"Rp {costs[cc]:,.0f}")

        diff = max(costs.values()) - min(costs.values())
        self.cards["Selisih Maks"].update_value(f"Rp {diff:,.0f}")
        self.cards["Error Taylor"].update_value("0.0000")

        # Update param labels
        for cc, m in models.items():
            if cc in self._param_labels:
                self._param_labels[cc].config(
                    text=f"a={m.a:.5f}  b={m.b:.4f}")

        # Redraw chart
        ax = self._ax
        ax.clear()
        vs = np.linspace(30, 80, 200)
        for cc, m in models.items():
            col = MOTOR_COLORS[cc]
            ax.plot(vs, [m.taylor(v) for v in vs],
                    color=col, linewidth=2.2, label=cc)
            ax.scatter([speed], [m.taylor(speed)], color=col, s=60, zorder=5)

        ax.set_facecolor(C_CHART_BG)
        ax.set_xlabel("Kecepatan (km/jam)", color=C_TEXT_DIM, fontsize=8)
        ax.set_ylabel("Konsumsi (l/km)",    color=C_TEXT_DIM, fontsize=8)
        ax.tick_params(colors=C_TEXT_DIM, labelsize=7)
        for sp in ax.spines.values():
            sp.set_edgecolor(C_BORDER)
        ax.legend(facecolor=C_CARD, edgecolor=C_BORDER,
                  labelcolor=C_TEXT, fontsize=8)
        ax.grid(True, color=C_BORDER, alpha=0.5, linestyle="--")
        self._fig.tight_layout(pad=1.2)
        self._canvas.draw()
