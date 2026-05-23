#!/bin/bash

set -e

echo "🗄️ Running database migrations..."

cd apps/api

# Wait for database to be ready
echo "⏳ Waiting for database..."
python -c "
import subprocess
import time
for i in range(30):
    try:
        result = subprocess.run(['psql', '-U', 'ai_user', '-h', 'db', '-c', 'SELECT 1'],
                              capture_output=True, timeout=1)
        if result.returncode == 0:
            print('✅ Database is ready')
            break
    except:
        pass
    time.sleep(1)
"

# Run migrations
echo "📝 Running Alembic migrations..."
python -m alembic upgrade head

echo "✅ Migrations complete!"
