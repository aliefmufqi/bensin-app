# ============================================================
#  ui/widgets.py — Komponen UI kustom yang dapat digunakan ulang
# ============================================================

import tkinter as tk
from config import *


class GlowButton(tk.Canvas):
    """Tombol dengan efek glow/outline berwarna."""

    def __init__(self, master, text, command=None, color=C_ACCENT,
                 width=160, height=40, font_size=10, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg=C_PANEL, highlightthickness=0, **kwargs)
        self.command   = command
        self.color     = color
        self.text      = text
        self.w         = width
        self.h         = height
        self.font_size = font_size
        self._draw(False)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw(self, hover):
        self.delete("all")
        w, h = self.w, self.h
        # Tkinter hanya mendukung #RRGGBB (6 karakter), bukan #RRGGBBAA
        fill = self.color if hover else C_CARD
        self.create_rectangle(
            3, 3, w - 3, h - 3,
            outline=self.color,
            width=2 if hover else 1,
            fill=fill,
        )
        text_color = C_BG if hover else self.color
        self.create_text(w // 2, h // 2, text=self.text,
                         fill=text_color,
                         font=("Segoe UI", self.font_size, "bold"))

    def _on_enter(self, e): self._draw(True)
    def _on_leave(self, e): self._draw(False)
    def _on_click(self, e):
        if self.command:
            self.command()


class MetricCard(tk.Frame):
    """Kartu metrik satu nilai dengan label dan garis aksen."""

    def __init__(self, master, title, value, unit, color=C_ACCENT, **kwargs):
        super().__init__(master, bg=C_CARD, padx=16, pady=12, **kwargs)

        tk.Label(self, text=title.upper(), bg=C_CARD, fg=C_TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")

        val_row = tk.Frame(self, bg=C_CARD)
        val_row.pack(anchor="w", pady=(4, 0))

        self._val_lbl = tk.Label(val_row, text=value, bg=C_CARD, fg=color,
                                 font=("Segoe UI", 22, "bold"))
        self._val_lbl.pack(side="left")

        tk.Label(val_row, text=" " + unit, bg=C_CARD, fg=C_TEXT_DIM,
                 font=("Segoe UI", 9)).pack(side="left", pady=(8, 0))

        tk.Frame(self, bg=color, height=2).pack(fill="x", pady=(8, 0))

    def update_value(self, value: str):
        self._val_lbl.config(text=value)


class SectionDivider(tk.Frame):
    """Label judul seksi dengan garis horizontal."""

    def __init__(self, master, text, **kwargs):
        super().__init__(master, bg=C_BG, **kwargs)
        tk.Label(self, text=text, bg=C_BG, fg=C_ACCENT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Frame(self, bg=C_BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(10, 0))


class Tooltip:
    """Tooltip kecil yang muncul saat hover widget."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text   = text
        self._tip   = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, e=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, bg="#1A2E45", fg=C_TEXT,
                 font=("Segoe UI", 9), padx=8, pady=4).pack()

    def _hide(self, e=None):
        if self._tip:
            self._tip.destroy()
            self._tip = None
