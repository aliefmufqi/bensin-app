# ============================================================
#  main.py — Entry point: merakit semua modul menjadi aplikasi
# ============================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from config import *
from core.model import FuelModel
from ui.sidebar import Sidebar
from ui.pages.dashboard  import DashboardPage
from ui.pages.calculator import CalculatorPage
from ui.pages.chart      import ChartPage
from ui.pages.table      import TablePage
from ui.pages.about      import AboutPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(*APP_MINSIZE)
        self.configure(bg=C_BG)

        self._models: dict[str, FuelModel] = {}
        self._pages:  dict[str, tk.Frame]  = {}
        self._active_tab = ""

        self._apply_style()
        self._build_topbar()
        self._build_body()
        self._compute_models()

        # Tampilkan halaman pertama
        self._navigate("dashboard")

    # ── ttk Style ────────────────────────────────────────────
    def _apply_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
                     background=C_CARD, foreground=C_TEXT,
                     fieldbackground=C_CARD, rowheight=30,
                     font=("Segoe UI", 9))
        s.configure("Treeview.Heading",
                     background=C_BORDER, foreground=C_ACCENT,
                     font=("Segoe UI", 9, "bold"))
        s.map("Treeview", background=[("selected", C_HOVER)])
        s.configure("Vertical.TScrollbar",
                     background=C_BORDER, troughcolor=C_PANEL,
                     arrowcolor=C_ACCENT)
        s.configure("Horizontal.TScrollbar",
                     background=C_BORDER, troughcolor=C_PANEL,
                     arrowcolor=C_ACCENT)

    # ── Top bar ──────────────────────────────────────────────
    def _build_topbar(self):
        # ── Top bar ──────────────────────────────────────────
        bar = tk.Frame(self, bg=C_PANEL, height=72)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Icon badge (kotak berwarna)
        icon_bg = tk.Frame(bar, bg=C_ACCENT, width=52, height=52)
        icon_bg.pack(side="left", padx=(20, 14))
        icon_bg.pack_propagate(False)
        tk.Label(icon_bg, text="⛽", bg=C_ACCENT, fg=C_BG,
                 font=("Segoe UI", 24)).place(relx=0.5, rely=0.5, anchor="center")

        # Title + subtitle
        txt_block = tk.Frame(bar, bg=C_PANEL)
        txt_block.pack(side="left")
        tk.Label(txt_block, text="FUEL ESTIMATOR", bg=C_PANEL, fg=C_TEXT,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(txt_block,
                 text="Analisis Estimasi Pengeluaran BBM  •  Metode Numerik Deret Taylor  •  Universitas Siliwangi 2026",
                 bg=C_PANEL, fg=C_TEXT_DIM, font=("Segoe UI", 8)).pack(anchor="w", pady=(3, 0))

        # Divider vertikal
        tk.Frame(bar, bg=C_BORDER, width=1).pack(side="left", fill="y", padx=22, pady=14)

        # Badge chips
        badge_frame = tk.Frame(bar, bg=C_PANEL)
        badge_frame.pack(side="left")
        for label, color in [("Deret Taylor", C_ACCENT), ("Orde-1", C_ACCENT2), ("Python", C_ACCENT3)]:
            chip = tk.Frame(badge_frame, bg=color, padx=10, pady=3)
            chip.pack(side="left", padx=(0, 6))
            tk.Label(chip, text=label, bg=color, fg=C_BG,
                     font=("Segoe UI", 8, "bold")).pack()

        # Jam + tanggal (kanan, 2 baris)
        right = tk.Frame(bar, bg=C_PANEL)
        right.pack(side="right", padx=28)
        self._date_lbl = tk.Label(right, bg=C_PANEL, fg=C_TEXT_DIM,
                                   font=("Segoe UI", 9), anchor="e")
        self._date_lbl.pack(anchor="e")
        self._time_lbl = tk.Label(right, bg=C_PANEL, fg=C_ACCENT,
                                   font=("Segoe UI", 16, "bold"), anchor="e")
        self._time_lbl.pack(anchor="e")
        self._tick()

        # Accent bar bawah — tiga warna
        accent_bar = tk.Frame(self, bg=C_BG, height=3)
        accent_bar.pack(fill="x")
        tk.Frame(accent_bar, bg=C_ACCENT,  height=3).pack(side="left", fill="both", expand=True)
        tk.Frame(accent_bar, bg=C_ACCENT2, height=3, width=120).pack(side="left")
        tk.Frame(accent_bar, bg=C_ACCENT3, height=3, width=60).pack(side="left")

    def _tick(self):
        now = datetime.now()
        self._date_lbl.config(text=now.strftime("%A, %d %B %Y"))
        self._time_lbl.config(text=now.strftime("%H:%M:%S"))
        self.after(1000, self._tick)

    # ── Body = sidebar + content ─────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=C_BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        self._sidebar = Sidebar(
            body,
            on_navigate=self._navigate,
            on_param_change=self._on_param_change,
        )
        self._sidebar.pack(side="left", fill="y", padx=(16, 0), pady=(16, 16))

        # Content area
        self._content = tk.Frame(body, bg=C_BG)
        self._content.pack(side="left", fill="both", expand=True,
                           padx=(0, 16), pady=(0, 16))

        # Buat semua halaman (tersembunyi dulu)
        self._pages["dashboard"]  = DashboardPage(
            self._content, self._get_models, self._get_params)
        self._pages["calculator"] = CalculatorPage(self._content)
        self._pages["chart"]      = ChartPage(
            self._content, self._get_models, self._get_params)
        self._pages["table"]      = TablePage(
            self._content, self._get_models, self._get_params)
        self._pages["about"]      = AboutPage(self._content)

    # ── Model ────────────────────────────────────────────────
    def _compute_models(self):
        for cc, (e1, e2) in DEFAULTS.items():
            self._models[cc] = FuelModel(cc, e1, e2)

    def _get_models(self):
        return self._models

    def _get_params(self):
        return self._sidebar.get_params()

    # ── Navigasi ─────────────────────────────────────────────
    def _navigate(self, tab: str):
        # Sembunyikan semua
        for page in self._pages.values():
            page.pack_forget()

        # Tampilkan halaman yang dipilih
        page = self._pages[tab]
        page.pack(fill="both", expand=True)
        self._sidebar.activate(tab)
        self._active_tab = tab

        # Refresh data sesuai halaman
        if tab == "dashboard":
            page.refresh()
        elif tab == "chart":
            page.refresh()
        elif tab == "table":
            page.refresh()

    # ── Saat parameter global berubah ────────────────────────
    def _on_param_change(self):
        try:
            self._get_params()   # validasi input dulu
        except ValueError:
            return               # abaikan jika belum valid

        if self._active_tab == "dashboard":
            self._pages["dashboard"].refresh()
        elif self._active_tab == "chart":
            self._pages["chart"].refresh()
        elif self._active_tab == "table":
            self._pages["table"].refresh()


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
