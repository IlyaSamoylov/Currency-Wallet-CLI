from valutatrade_hub.core.usecases import (
	buy,
	get_rate,
	login,
	register,
	sell,
	show_portfolio,
)
from valutatrade_hub.core.utils import init_data_files


def print_help(command=None):
	helps = {
		"register": "register --username <username> --password <password>",
		"login": "login --username <username> --password <password>",
		"buy": "buy --currency <currency> --amount <amount>",
		"sell": "sell --currency <currency> --amount <amount>",
		"show-portfolio": "show-portfolio [--base <base> = USD]",
		"get-rate": "get-rate --from <from currency> --to <to currency>",
	}
	if command and command in helps:
		print(helps[command])
	else:
		print("Доступные команды:")
		for name, example in helps.items():
			print(f"  {name:15} → {example}")



# TODO: закончить run()
def run():
	init_data_files()
	print("Добро пожаловать")
	print_help()
	while True:
		full_command = input(">").strip().split("--")
		command = full_command[0].strip()
		params = {el.strip().split()[0]: el.strip().split()[1] for el
																	in full_command[1:]}

		try:
			match command:
				case "register":
					register(**params)

				case "login":
					login(**params)

				case "show-portfolio":
					show_portfolio(**params)

				case "buy":
					params["amount"] = float(params["amount"])
					buy(**params)

				case "sell":
					params["amount"] = float(params["amount"])
					sell(**params)

				case "get-rate":
					get_rate(**params)

				case "help":
					print_help(**params)

				case "exit":
					break

				case _:
					print("Неизвестная команда")


		# except TypeError:
		# 	print("Проверьте правильность и количество параметров. Можете обратиться к"
		# 	      " справке, вызвав help для полной справки или help --command <command>
		# 	      " для справки по отдельной команде")

		except IndexError:
			print("Вводите сначала имя переменной с --, потом значение")

		# except Exception as e:
		# 	print(f"ошибка {e}")
