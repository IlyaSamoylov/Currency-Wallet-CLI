# выбрасывается в Wallet.withdraw() и/или в usecases.sell()
class InsufficientFundsError(Exception):
	def __init__(self, message, available:float, required:float, code:str = 'USD'):
		super().__init__(message)   # Зачем message? Обязательно ли использовать в выводе?
		self.available = available
		self.required = required
		self.code = code

	def __str__(self):
		return (f"Недостаточно средств: доступно {self.available} {self.code},"
		        f" требуется {self.required} {self.code}")

# Выбрасывается в currencies.get_currency() и при валидации входа в get-rate.
class CurrencyNotFoundError(Exception):
	def __init__(self, message, code):
		super().__init__(message)
		self.code = code

	def __str__(self):
		return f"Неизвестная валюта '{self.code}"

# Выбрасывается в слое получения курсов (заглушка/Parser Service).
class ApiRequestError(Exception):
	def __init__(self, message):
		super().__init__(message)   #Правильно? Что я передал? А может, init вообще здесь не нужен?
	def __str__(self):
		return f"Ошибка при обращении к внешнему API: {self.args[0]}"   # Правильно? Что такое self.args[0]?

#  Обновить раздел «Ошибки» у соответствующих команд CLI.
