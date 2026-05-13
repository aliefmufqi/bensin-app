# ============================================================
#  core/model.py — Mesin perhitungan Metode Numerik Deret Taylor
# ============================================================


class FuelModel:
    """
    Model konsumsi bahan bakar menggunakan Deret Taylor Orde-1.

    Langkah-langkah:
      1. Konversi efisiensi km/L → konsumsi l/km  : C(v) = 1 / eff
      2. Bangun model linear dari 2 titik data     : C(v) = av + b
      3. Aproksimasi Deret Taylor orde-1           : C(v) ≈ C(v₀) + C'(v₀)(v−v₀)
    """

    def __init__(self, cc: str, eff_v1: float, eff_v2: float,
                 v1: float = 50, v2: float = 60):
        self.cc = cc
        self.v1 = v1
        self.v2 = v2

        # Langkah 1 — konversi km/L → l/km
        self.C1 = 1.0 / eff_v1
        self.C2 = 1.0 / eff_v2

        # Langkah 2 — hitung gradien (a) dan konstanta (b)
        self.a = (self.C2 - self.C1) / (self.v2 - self.v1)
        self.b = self.C1 - self.a * self.v1

        # Titik pusat ekspansi Taylor
        self.v0 = v1

    # ── Model linear asli ──────────────────────────────────
    def linear(self, v: float) -> float:
        """C(v) = av + b"""
        return self.a * v + self.b

    # ── Aproksimasi Deret Taylor orde-1 ───────────────────
    def taylor(self, v: float) -> float:
        """C(v) ≈ C(v₀) + C'(v₀)(v − v₀)"""
        return self.linear(self.v0) + self.a * (v - self.v0)

    # ── Estimasi biaya harian ─────────────────────────────
    def daily_cost(self, v: float, distance_km: float, price_per_liter: float):
        """
        Mengembalikan (volume_liter, biaya_rupiah) per hari.
        Volume = C(v) × jarak
        Biaya  = Volume × harga
        """
        volume = self.taylor(v) * distance_km
        cost   = volume * price_per_liter
        return volume, cost

    # ── Error aproksimasi ─────────────────────────────────
    def error_absolute(self, v: float) -> float:
        """|C_Taylor(v) - C_Linear(v)|  → 0 untuk fungsi linear"""
        return abs(self.taylor(v) - self.linear(v))
