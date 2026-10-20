"""Initialize demo data only when no database exists."""
from pathlib import Path
from database import create_database, seed_events, seed_users

if __name__ == '__main__':
    path = Path(__file__).resolve().parent / 'database.db'
    if path.exists():
        raise SystemExit('database.db already exists. Existing data was not changed.')
    create_database()
    seed_events()
    seed_users()
    print('Ready. Run: python app.py')
