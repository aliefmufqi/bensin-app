@echo off
REM ============================================================
REM  build.bat — Build aplikasi menjadi .exe (jalankan di Windows)
REM ============================================================

echo [1/3] Install dependencies...
pip install -r requirements.txt

echo [2/3] Build executable...
pyinstaller --onefile --windowed ^
  --name "FuelEstimator_Siliwangi" ^
  --add-data "core;core" ^
  --add-data "ui;ui" ^
  main.py

echo [3/3] Selesai! File .exe ada di folder: dist\
pause
