import abc
from abc import ABC, abstractmethod

class Currency(ABC):
	def __init(self, name:str, code:str):
		self.name = name
		self.code = code

	# Надо еще как-то сделать валидацию параметров

	@abstractmethod
	def get_display_info(self) -> str:
		pass

class FiatCurrency(Currency):
	def __init__(self, name, code, issuing_country):
		super().__init__(name, code)
		self.issuing_country = issuing_country

	def get_display_info(self) -> str:
		return f"[FIAT] {self.code} — {self.name} (Issuing: {self.issuing_country})"

class CryptoCurrency(Currency):
	def __init__(self, name, code, algorithm, market_cap):
		super().__init__(name, code)
		self.algorithm = algorithm
		self.market_cap = market_cap

	def get_display_info(self) -> str:
		return (f"[CRYPTO] {self.code} — {self.name} (Algo: {self.algorithm}, "
		        f"MCAP: {self.market_cap})")

# 3. Добавить фабричный метод get_currency() и правила обработки неизвестных кодов.


