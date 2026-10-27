import sys
import os
from pathlib import Path
import uvicorn

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import settings

if __name__ == "__main__":
    print("=" * 70)
    print("🛡️  SSLGuard — SSL Certificate Monitoring & WhatsApp Alert System")
    print("   Dinas Komunikasi dan Informatika (KOMINFO) | PKL 2026")
    print("=" * 70)
    print(f"📡 API Base URL     : http://127.0.0.1:8000{settings.API_V1_STR}")
    print("📑 Swagger Docs     : http://127.0.0.1:8000/docs")
    print("🌐 Dashboard UI     : http://127.0.0.1:8000/")
    print("⏰ Daily Scheduler  : Active (07:00 WIB)")
    print("=" * 70)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
