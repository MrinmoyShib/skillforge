#!/bin/sh
set -e

echo "==> [SkillForge] Waiting for PostgreSQL database..."
python << END
import time
import sys
import psycopg2
import os

db_url = os.environ.get("DATABASE_URL", "")
for attempt in range(30):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("==> [SkillForge] PostgreSQL is ready!")
        sys.exit(0)
    except Exception as e:
        print(f"Waiting for database ({attempt + 1}/30)...")
        time.sleep(1)
print("==> [SkillForge] ERROR: Could not connect to database.")
sys.exit(1)
END

# NOTE: Database migrations and collectstatic should be run as a separate
# one-time release/deploy step, NOT during container startup.
# This prevents race conditions when scaling horizontally.
# Run manually: docker exec skillforge-django python manage.py migrate

echo "==> [SkillForge] Starting service: $@"
exec "$@"

