# Проект 3 - Консольное приложение: имитация валютного кошелька

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Poetry](https://img.shields.io/badge/Poetry-управление_зависимостями-orange)

Программа представляет собой консольное приложение, имитирующее работу валютного кошелька. Поддерживает регистрацию, вход в аккаунт, просмотр кошелька, покупку и продажу валюты, просмотр текущего курса (на данный момент заглушка, но в скором времени будет парсер). Хранит данные о зарегистрированных пользователях, портфелях, курсе и сессии в соответствующих json.

## Установка и запуск

## Быстрый старт

### Предварительные требования

- Python 3.12 или выше
- Poetry (менеджер зависимостей)
- Make 

### Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/IlyaSamoylov/finalproject_Samoylov_M25-555
   cd finalproject_Samoylov_M25-555
   ```

2. **Установите poetry (если не установлен)**
   ### Windows
   pip install poetry

   ### Linux/macOS
   sudo apt install python3-poetry

3. **Настройте poetry, чтобы он создавал виртуальные окружения в директории проекта**
  ```bash
   poetry config virtualenvs.in-project true  
  ```
4. **Установите зависимости проекта**
  ```bash
  poetry install
  ```
  или 
  ```bash
  make install
  ```
5. **Активируйте виртуальное окружение**
  ### Linux
  ```bash
  source .venv/bin/activate
  ```
  ### Windows
  ```bash
  source .venv/Scripts/activate
  ```
6. **Начните использовать**
   ## через make:
   ```bash
    make run
   ```
   ## через poetry:
   ```bash
   poetry run project
   ```

## Доступные команды (usecases):


| Команда                                                | Описание                                                          |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| `register --username <username> --password <password>` | зарегистрироваться                                                |
| `login --username <username> --password <password>`    | войти в аккаунт                                                   |
| `buy --currency <currency> --amount <amount>`          | купить валюты `currency` в количестве `amount`                    |
| `sell --currency <currency> --amount <amount>`         | продать валюты `currency` в количестве `amount`                   |
| `show-portfolio [--base <base> = USD]`                 | показать портфель пользователя, все перевести в валюту `currency` |
| `get-rate --from <from currency> --to <to currency>`   | показать курс `from_v` -> `to`                                    |
| `help`                                                 | справочная информация                                             |
| `exit`                                                 | выйти из программы                                                |

Поддерживаемые сейчас валюты (`currency`): `USD`, `RUB`, `BTC`, `ETH`, `EUR`.

## Файлы данных
### `users.json`
Хранит информацию о зарегистрированных пользователях: их id, никнейм, хэш пароля, соль, дата регистрации

### `portfolio.json`
Хранит портфели пользователей: id пользователя и кошельки 

### `rates.json`
Хранит курсы и дату последнего обновления 

### `session.json`
Хранит id и ник последнего авторизованного пользователя
## Пример работы
```
$ poetry run project
Добро пожаловать
Доступные команды:
  register        → register --username <username> --password <password>
  login           → login --username <username> --password <password>
  buy             → buy --currency <currency> --amount <amount>
  sell            → sell --currency <currency> --amount <amount>
  show-portfolio  → show-portfolio [--base <base> = USD]
  get-rate        → get-rate --from <from currency> --to <to currency>
>register --username Volodya --password 1111
Пользователь 'Volodya' зарегистрирован (id=3). Войдите: login --username Volodya --password ****
>login --username Volodya --password 1111
Вы вошли как 'Volodya'
>show-portfolio
Портфель пуст
>buy --currency ETH --amount 1
>sell --currency ETH --amount 0.5
>show-portfolio
Портфель пользователя 'Volodya' (база: USD):
- ETH: 0.5 -> 1860.0
----------
ИТОГО: 1860.0 USD
>get-rate --from_v ETH --to USD
Нет данных и недоступен Parser ->
Курс ETH->USD недоступен. Повторите позже
>exit
```