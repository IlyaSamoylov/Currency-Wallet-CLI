from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
# ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

USERS_DIR = DATA_DIR / "users.json"
PORTFOLIOS_DIR = DATA_DIR / "portfolios.json"
RATES_DIR = DATA_DIR / "rates.json"

SESSION_FILE = DATA_DIR / "session.json" #Path("data/session.json")

VALUTA = ["USD", "RUB", "BTC", "ETH", "EUR"]


