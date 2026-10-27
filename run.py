"""
SSLGuard Main Root Runner
Starts the entire SSLGuard application (Backend REST API + Frontend SPA + Scheduler)
Usage:
    python run.py
"""
import sys
import os
import subprocess
from pathlib import Path
import webbrowser

root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"
venv_python = root_dir / "venv" / "Scripts" / "python.exe"

python_bin = str(venv_python) if venv_python.exists() else sys.executable

# Auto-seed database if not present
db_file = root_dir / "sslguard.db"
if not db_file.exists():
    print("📦 Basis data sslguard.db belum terdeteksi. Menjalankan seeder otomatis...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir)
    subprocess.run([python_bin, str(backend_dir / "seed_data.py")], cwd=str(root_dir), env=env)

print("\n" + "=" * 70)
print("🛡️  SSLGuard — KOMINFO PKL 2026")
print("   Sistem Pemantauan SSL/TLS & Notifikasi Peringatan Dini WhatsApp")
print("=" * 70)
print("🚀 Menjalankan Server Backend FastAPI...")
print("🌐 Dashboard Aplikasi : http://localhost:8000/")
print("📑 Dokumentasi API    : http://localhost:8000/docs")
print("=" * 70 + "\n")

# Start server using backend runner
env = os.environ.copy()
env["PYTHONPATH"] = str(backend_dir)
try:
    subprocess.run([python_bin, str(backend_dir / "run.py")], cwd=str(root_dir), env=env)
except KeyboardInterrupt:
    print("\n🛑 SSLGuard Server dihentikan.")
