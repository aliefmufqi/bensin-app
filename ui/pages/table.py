# ============================================================
#  ui/pages/table.py — Halaman Tabel Data Lengkap
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import csv
from datetime import datetime

from config import *
from ui.widgets import GlowButton


class TablePage(tk.Frame):
    def __init__(self, master, get_models, get_params):
        super().__init__(master, bg=C_BG)
        self.get_models = get_models
        self.get_params = get_params
        self._build()

    # ── Build layout ─────────────────────────────────────────
    def _build(self):
        tk.Label(self, text="Tabel Data Lengkap", bg=C_BG, fg=C_TEXT,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(16, 4))

        # Toolbar
        tb = tk.Frame(self, bg=C_BG)
        tb.pack(fill="x", pady=(0, 8))
        GlowButton(tb, "⬇  Export CSV", self._export,
                   color=C_ACCENT2, width=140, height=34).pack(side="left", padx=(0, 8))
        GlowButton(tb, "🔄  Refresh", self.refresh,
                   color=C_ACCENT, width=120, height=34).pack(side="left")
        tk.Label(tb, text="Rentang kecepatan: 30–80 km/h, step 5",
                 bg=C_BG, fg=C_TEXT_DIM, font=("Segoe UI", 8)).pack(side="right")

        # Treeview
        columns = [
            "v (km/h)",
            "C_lin 110", "C_tay 110", "Err 110",
            "C_lin 125", "C_tay 125", "Err 125",
            "C_lin 150", "C_tay 150", "Err 150",
            "Biaya 110",  "Biaya 125",  "Biaya 150",
        ]
        self._tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self._tree.heading(col, text=col)
            w = 70 if col.startswith("v") else 82
            self._tree.column(col, width=w, anchor="center", minwidth=60)

        sb_h = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        sb_v = ttk.Scrollbar(self, orient="vertical",   command=self._tree.yview)
        self._tree.configure(xscrollcommand=sb_h.set, yscrollcommand=sb_v.set)
        sb_v.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)
        sb_h.pack(fill="x")

    # ── Refresh tabel ────────────────────────────────────────
    def refresh(self):
        try:
            dist, price, _ = self.get_params()
            models = self.get_models()
        except Exception:
            return

        for row in self._tree.get_children():
            self._tree.delete(row)

        odd = True
        for v in np.arange(30, 85, 5):
            row = [f"{v:.0f}"]
            for m in models.values():
                row += [f"{m.linear(v):.6f}",
                        f"{m.taylor(v):.6f}",
                        f"{m.error_absolute(v):.6f}"]
            for m in models.values():
                _, cost = m.daily_cost(v, dist, price)
                row.append(f"Rp {cost:,.0f}")
            tag = "odd" if odd else "even"
            self._tree.insert("", "end", values=row, tags=(tag,))
            odd = not odd

        self._tree.tag_configure("odd",  background=C_CARD)
        self._tree.tag_configure("even", background=C_PANEL)

    # ── Export CSV ───────────────────────────────────────────
    def _export(self):
        try:
            dist, price, _ = self.get_params()
            models = self.get_models()
        except Exception:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Simpan Data ke CSV")
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Fuel Estimator — Metode Numerik Deret Taylor"])
            w.writerow([f"Diekspor: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            w.writerow([])
            w.writerow(["v(km/h)",
                         "C_lin_110", "C_tay_110", "err_110",
                         "C_lin_125", "C_tay_125", "err_125",
                         "C_lin_150", "C_tay_150", "err_150",
                         "biaya_110", "biaya_125", "biaya_150"])
            for v in np.arange(30, 85, 5):
                row = [v]
                for m in models.values():
                    row += [round(m.linear(v), 6),
                            round(m.taylor(v), 6),
                            round(m.error_absolute(v), 6)]
                for m in models.values():
                    _, c = m.daily_cost(v, dist, price)
                    row.append(round(c, 2))
                w.writerow(row)

        messagebox.showinfo("Berhasil", f"Data disimpan ke:\n{path}")
