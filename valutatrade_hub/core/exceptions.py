class ValutaTradeError(Exception):
	pass

class InsufficientFundsError(ValutaTradeError):
	def __init__(self, available :float, code: str, required: float):
		super().__init__(f"Недостаточно средств: доступно {available:.8f} {code}, "
		                 f"требуется {required:.8f} {code}")

		self.available = available
		self.code = code
		self.req_funds = required

class CurrencyNotFoundError(ValutaTradeError):
	def __init__(self, code:str):
		super().__init__(f"Неизвестная валюта '{code}'")
		self.code = code

class ApiRequestError(ValutaTradeError):
	def __init__(self, reason: str):
		super().__init__(f"Ошибка при обращении к внешнему API: {reason}")
		self.reason = reason

class WalletNotFoundError(ValutaTradeError):
	def __init__(self, currency: str):
		super().__init__(f"Отсутствует кошелек '{currency}'")
		self.currency = currency
