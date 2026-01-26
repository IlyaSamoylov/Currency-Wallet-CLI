import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, Iterable

from valutatrade_hub.parser_service.config import ParserConfig


class RatesStorage:
	def __init__(self, config: ParserConfig):
		self._rates_path = Path(config.RATES_FILE_PATH)
		self._history_path = Path(config.HISTORY_FILE_PATH)
		self._lock = threading.RLock()

	def save_rates(self, data: Dict[str, Any]) -> None:
		with self._lock:
			self._rates_path.parent.mkdir(parents=True, exist_ok=True)
			self._atomic_write(self._rates_path, data)

	def load_rates(self):
		with self._lock:
			if not os.path.exists(self._rates_path):
				return {"pairs": {}, "last_refresh": None}

			with open(self._rates_path, "r", encoding="utf-8") as f:
				return json.load(f)


	def append_history(self, records: Iterable[Dict[str, Any]]) -> None:
		with self._lock:
			self._history_path.parent.mkdir(parents=True, exist_ok=True)

			if self._history_path.exists():
				try:
					with open(self._history_path, "r", encoding="utf-8") as f:
						history = json.load(f)
					if not isinstance(history, list):
						history = []
				except (json.JSONDecodeError, OSError):
					history = []
			else:
				history = []

			history.extend(records)
			self._atomic_write(self._history_path, history)

	def _atomic_write(self, path: Path, data: Any) -> None:
		tmp = path.with_suffix(".tmp")
		with open(tmp, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
		tmp.replace(path)