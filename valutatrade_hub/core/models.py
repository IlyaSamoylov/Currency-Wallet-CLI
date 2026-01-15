from __future__ import annotations

from datetime import datetime
import hashlib
import json

from utils import generate_salt
from valutatrade_hub.constants import PORTFOLIOS_DIR, RATES_DIR, USERS_DIR

class User:
	# todo: убедиться, что User будут передаваться правильные форматы date/password
	def __init__(self, user_id: int, username: str, password: str,
				registration_date: datetime | None = None):

		# TODO: user_id должен быть уникальным, это будет контролироваться в usecases
		self._user_id = user_id
		# _username устанавливается через setter - внутри валидируется:
		self.username = username
		self._salt = self._generate_salt()
		# пароль валидируется в приватном методе, а затем в другом из него делается хэш
		self._hashed_password = self._hash(self._validate_pword(password))
		# дата регистрации устанаваливается как передана, если не передана, то устанавливается сейчас
		self._registration_date = registration_date if registration_date is not None \
			else datetime.now()

	@property
	def user_id(self):
		return self._user_id

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, uname: str):
		# валидация username
		if not isinstance(uname, str) or not uname.strip():
			raise ValueError("Имя не может быть пустым")

		self._username = uname

	@property
	def hashed_password(self):
		return self._hashed_password

	@property
	def salt(self):
		return self._salt

	@property
	def registration_date(self):
		return self._registration_date

	def get_user_info(self):
		return {
			"User ID": self.user_id,
			"Username": self.username,
			"Registration Date": self.registration_date
		}

	def _validate_pword(self, pword: str):
		# валидация введенного пароля
		if not isinstance(pword, str) or len(pword.strip()) < 4:
			raise ValueError("Неверный формат password")
		return pword

	def _generate_salt(self):
		return generate_salt()

	def change_password(self, new_password: str):
		self._salt = self._generate_salt()
		self._hashed_password = self._hash(self._validate_pword(new_password))

	def verify_password(self, password: str):
		return self._hash(password) == self._hashed_password

	def _hash(self, password: str) -> str:
		return hashlib.sha256(password.encode() + self._salt.encode()).hexdigest()

	@classmethod
	def from_dict(cls, u_dict) -> User:
		user = cls.__new__(cls)

		user._user_id = u_dict["user_id"]
		user._username = u_dict["username"]
		user._hashed_password = u_dict["hashed_password"]
		user._salt = u_dict["salt"]
		user._registration_date = datetime.fromisoformat(
			u_dict["registration_date"]
		)

		return user

	def to_dict(self):
		u_dict = {
			"user_id": self.user_id,
			"username": self.username,
			"hashed_password": self.hashed_password,
			"salt": self.salt,
			"registration_date": self.registration_date.fromisoformat()
		}
		return u_dict

class Wallet:
	def __init__(self, currency_code: str, _balance: float):
		self.currency_code = currency_code
		self._balance = _balance

	def deposit(self, amount:float):
		if not isinstance(amount, (int, float)):
			raise ValueError("'Количество' денег должно быть числом")
		if amount < 0:
			raise ValueError("Нельзя положить отрицательное количество денег")

		self._balance += amount

	def withdraw(self, amount:float):
		if amount <= 0:
			raise ValueError("Сумма снятие не может быть меньше или равна 0")
		if amount > self.balance:
			raise ValueError("Сумма снятия не может превышать баланс")
		self._balance -= amount

	def get_balance_info(self):
		return {
			"Currency code": self.currency_code,
			"Balance": self._balance
		}

	@property
	def balance(self):
		return self._balance

	@balance.setter
	def balance(self, value: float):
		if value < 0:
			raise ValueError("Баланс не может быть меньше 0")
		if not isinstance(value, (int, float)):
			raise ValueError("Некорректный тип данных")
		self._balance = value

class Portfolio:
	def __init__(self, user_id: int, _wallets: dict[str, Wallet]):
		self._user_id = user_id
		self._wallets = _wallets

	def add_currency(self, currency_code: str):
		if currency_code in self._wallets.keys():
			raise ValueError("Такой кошелек в портфеле уже есть")
		self._wallets[currency_code] = Wallet(currency_code, 0)

	def get_total_value(self, base_currency: str ='USD'):
		try:
			with open(PORTFOLIOS_DIR, "r") as f:
				portfolios_list = json.load(f)
				user_portf = [port for port in portfolios_list if port["user_id"]
																	== self._user_id]
		except FileNotFoundError:
			print("Файл с данными о портфелях не существует")

		try:
			with open(RATES_DIR, "r") as f:
				rates_dict = json.load(f)
		except FileNotFoundError:
			print("Файл с данными о курсах валют не существует")

		if not user_portf:
			print("Пользователь с таким id не отслеживается")
			return 0

		total = 0

		for valuta, balance_info in user_portf[0]["wallets"].items():
			total += balance_info["balance"] * rates_dict[valuta][base_currency]

		return total

	def get_wallet(self, currency_code):
		# сначала проверяем в памяти
		w = self._wallets.get(currency_code)
		if w:
			return w

		# попытка подгрузить из файла portfolios.json
		try:
			with open(PORTFOLIOS_DIR, "r", encoding="utf-8") as f:
				portfolios = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError("Файл portfolios.json не найден")

		portfolio = next((p for p in portfolios if p.get("user_id") == self._user_id),
																				None)
		if not portfolio:
			raise ValueError(
				"Портфель для пользователя с id={} не найден".format(self._user_id))

		wallets_dict = portfolio.get("wallets", {})
		w_data = wallets_dict.get(currency_code)
		if not w_data:
			raise ValueError("Кошелёк с кодом {} не найден".format(currency_code))

		wallet_obj = Wallet(currency_code=w_data.get("currency_code", currency_code),
													_balance=float(w_data["balance"]))
		# кэшируем в self._wallets
		self._wallets[currency_code] = wallet_obj
		return wallet_obj

	@property
	def user(self):
		try:
			with open(USERS_DIR, "r") as f:
				users_dict = json.load(f)
			user_list = [user for user in users_dict if user["user_id"]
                                                                    == self._user_id]

		except FileNotFoundError:
			print("Файл с данными пользователей не найден")

		if not user_list:
			print("Пользователя с таким id нет в базе")

		user_dict = user_list[0]
		user_info = User(self._user_id, user_dict["username"],
						user_dict["hashed_password"], user_dict["salt"],
						user_dict["registration_date"])
		return user_info

	@property
	def wallets(self):
		return self._wallets.copy()




