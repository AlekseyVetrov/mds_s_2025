import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.database import init_db

if __name__ == "__main__":
    init_db()
    print("Готово")