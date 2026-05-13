# ============================================================
#  ui/pages/chart.py — Halaman Visualisasi Grafik
# ============================================================

import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from config import *


class ChartPage(tk.Frame):
    def __init__(self, master, get_models, get_params):
        super().__init__(master, bg=C_BG)
        self.get_models = get_models
        self.get_params = get_params
        self._chart_type = tk.StringVar(value="all")
        self._build()

    # ── Build layout ─────────────────────────────────────────
    def _build(self):
        tk.Label(self, text="Visualisasi Grafik", bg=C_BG, fg=C_TEXT,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(16, 4))

        # Selector tampilan
        ctrl = tk.Frame(self, bg=C_BG)
        ctrl.pack(fill="x", pady=(0, 8))
        tk.Label(ctrl, text="Tampilan:", bg=C_BG, fg=C_TEXT_DIM,
                 font=("Segoe UI", 9)).pack(side="left")
        for txt, val in [("Semua Grafik", "all"), ("Konsumsi", "cons"),
                         ("Biaya", "cost"), ("Perbandingan", "compare")]:
            tk.Radiobutton(ctrl, text=txt, variable=self._chart_type,
                           value=val, bg=C_BG, fg=C_TEXT,
                           selectcolor=C_CARD, activebackground=C_BG,
                           activeforeground=C_ACCENT,
                           font=("Segoe UI", 9),
                           command=self.refresh).pack(side="left", padx=8)

        # Canvas matplotlib
        self._fig = Figure(figsize=(10, 6.5), dpi=96, facecolor=C_CHART_BG)
        self._canvas = FigureCanvasTkAgg(self._fig, self)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)
        toolbar_frame = tk.Frame(self, bg=C_BG)
        toolbar_frame.pack(fill="x")
        NavigationToolbar2Tk(self._canvas, toolbar_frame)

    # ── Refresh ──────────────────────────────────────────────
    def refresh(self):
        try:
            dist, price, speed = self.get_params()
            models = self.get_models()
        except Exception:
            return

        vs  = np.linspace(30, 80, 300)
        fig = self._fig
        fig.clear()
        ctype = self._chart_type.get()

        if ctype == "all":
            gs   = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)
            axes = [fig.add_subplot(gs[0, 0], facecolor=C_CHART_BG),
                    fig.add_subplot(gs[0, 1], facecolor=C_CHART_BG),
                    fig.add_subplot(gs[1, 0], facecolor=C_CHART_BG),
                    fig.add_subplot(gs[1, 1], facecolor=C_CHART_BG)]
            self._draw_consumption(axes[0], vs, models)
            self._draw_cost(axes[1], vs, models, dist, price)
            self._draw_bar(axes[2], models, dist, price, speed)
            self._draw_sensitivity(axes[3], models, dist, price, speed)
        elif ctype == "cons":
            self._draw_consumption(fig.add_subplot(111, facecolor=C_CHART_BG), vs, models)
        elif ctype == "cost":
            self._draw_cost(fig.add_subplot(111, facecolor=C_CHART_BG), vs, models, dist, price)
        else:
            gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)
            self._draw_bar(fig.add_subplot(gs[0, 0], facecolor=C_CHART_BG),
                           models, dist, price, speed)
            self._draw_sensitivity(fig.add_subplot(gs[0, 1], facecolor=C_CHART_BG),
                                   models, dist, price, speed)

        fig.patch.set_facecolor(C_CHART_BG)
        self._canvas.draw()

    # ── Helper style ─────────────────────────────────────────
    def _style(self, ax, title, xlabel, ylabel):
        ax.set_title(title, color=C_TEXT, fontsize=9, fontweight="bold", pad=8)
        ax.set_xlabel(xlabel, color=C_TEXT_DIM, fontsize=8)
        ax.set_ylabel(ylabel, color=C_TEXT_DIM, fontsize=8)
        ax.tick_params(colors=C_TEXT_DIM, labelsize=7)
        for sp in ax.spines.values():
            sp.set_edgecolor(C_BORDER)
        ax.grid(True, color=C_BORDER, alpha=0.4, linestyle="--")

    # ── Chart 1: Konsumsi vs Kecepatan ───────────────────────
    def _draw_consumption(self, ax, vs, models):
        for cc, m in models.items():
            col = MOTOR_COLORS[cc]
            ax.plot(vs, [m.taylor(v) for v in vs],
                    color=col, linewidth=2, label=f"{cc} Taylor")
            ax.plot(vs, [m.linear(v) for v in vs],
                    color=col, linewidth=1, linestyle=":", alpha=0.5,
                    label=f"{cc} Linear")
        self._style(ax, "Konsumsi Bahan Bakar vs Kecepatan",
                    "Kecepatan (km/jam)", "Konsumsi (l/km)")
        ax.legend(facecolor=C_CARD, edgecolor=C_BORDER,
                  labelcolor=C_TEXT, fontsize=7, ncol=2)

    # ── Chart 2: Biaya Harian vs Kecepatan ───────────────────
    def _draw_cost(self, ax, vs, models, dist, price):
        for cc, m in models.items():
            col   = MOTOR_COLORS[cc]
            costs = [m.taylor(v) * dist * price for v in vs]
            ax.plot(vs, costs, color=col, linewidth=2, label=cc)
            ax.fill_between(vs, costs, alpha=0.08, color=col)
        self._style(ax, "Estimasi Biaya Harian vs Kecepatan",
                    "Kecepatan (km/jam)", "Biaya (Rp/hari)")
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"Rp{x/1000:.0f}k"))
        ax.legend(facecolor=C_CARD, edgecolor=C_BORDER,
                  labelcolor=C_TEXT, fontsize=8)

    # ── Chart 3: Bar perbandingan ─────────────────────────────
    def _draw_bar(self, ax, models, dist, price, speed):
        labels = list(models.keys())
        costs  = [models[cc].daily_cost(speed, dist, price)[1] for cc in labels]
        colors = [MOTOR_COLORS[cc] for cc in labels]
        bars   = ax.bar(labels, costs, color=colors, width=0.5, alpha=0.85)
        for bar, cost in zip(bars, costs):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                    f"Rp{cost:,.0f}", ha="center", va="bottom",
                    color=C_TEXT, fontsize=7, fontweight="bold")
        self._style(ax, f"Perbandingan Biaya Harian (@{speed:.0f} km/h)",
                    "Kapasitas Mesin", "Biaya (Rp/hari)")
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"Rp{x/1000:.0f}k"))

    # ── Chart 4: Sensitivitas harga ───────────────────────────
    def _draw_sensitivity(self, ax, models, dist, price, speed):
        pcts  = [0, 10, 20, 30, 50]
        x     = np.arange(len(pcts))
        width = 0.25
        for i, (cc, m) in enumerate(models.items()):
            costs = [m.daily_cost(speed, dist, price * (1 + p / 100))[1]
                     for p in pcts]
            ax.bar(x + i * width, costs, width,
                   color=MOTOR_COLORS[cc], label=cc, alpha=0.85)
        ax.set_xticks(x + width)
        ax.set_xticklabels([f"+{p}%" for p in pcts],
                           color=C_TEXT_DIM, fontsize=7)
        self._style(ax, "Sensitivitas Terhadap Kenaikan Harga BBM",
                    "Kenaikan Harga (%)", "Biaya (Rp/hari)")
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"Rp{x/1000:.0f}k"))
        ax.legend(facecolor=C_CARD, edgecolor=C_BORDER,
                  labelcolor=C_TEXT, fontsize=8)
