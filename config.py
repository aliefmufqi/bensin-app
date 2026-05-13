# ============================================================
#  config.py — Semua konstanta warna, font, dan data default
# ============================================================

# ── Colour Palette ──────────────────────────────────────────
C_BG        = "#0F1923"
C_PANEL     = "#162030"
C_CARD      = "#1C2B3A"
C_ACCENT    = "#00C8FF"
C_ACCENT2   = "#00FF9D"
C_ACCENT3   = "#FF6B35"
C_ACCENT4   = "#FFD700"
C_TEXT      = "#E8F4FD"
C_TEXT_DIM  = "#7A9BB5"
C_BORDER    = "#243548"
C_HOVER     = "#1E3550"
C_SUCCESS   = "#00E676"
C_CHART_BG  = "#111D2B"

MOTOR_COLORS = {
    "110cc": "#00C8FF",
    "125cc": "#00FF9D",
    "150cc": "#FF6B35",
}

# ── Default Efficiency Data (km/L) ──────────────────────────
# Format: { "cc_label": (efisiensi_@50kmh, efisiensi_@60kmh) }
DEFAULTS = {
    "110cc": (50, 45),
    "125cc": (45, 40),
    "150cc": (40, 35),
}

# ── App Info ────────────────────────────────────────────────
APP_TITLE   = "Fuel Estimator — Metode Numerik Deret Taylor  |  Universitas Siliwangi 2026"
APP_SIZE    = "1400x860"
APP_MINSIZE = (1100, 720)

TEAM_MEMBERS = [
    ("Alief Mufqi Alwany",       "247006111082"),
    ("Ilham Sutiyoso",            "247006111085"),
    ("Mohammad Rizal Ramadan",    "247006111112"),
    ("Muhammad Fauzan Gemilang",  "247006111154"),
]
