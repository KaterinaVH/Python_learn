from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk  # Импортируем виджеты (нам нужна для создания выпадающего списка)
from tkinter.font import BOLD

import requests  # Импортируем библиотеку для работы с запросами в интернет (API, JSON)


def center_window (window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def update_crypto_label(event):  # Функция вызывается при выборе криптовалюты
    code = crypto_combobox.get()  # Получаем выбранный код криптовалюты
    name = crypto_currencies[code]  # По коду находим полное название криптовалюты
    crypto_label.config(text=name)  # Подписываем название криптовалюты под списком


def exchange():  # Функция вызывается при нажатии на кнопку
    crypto_code = crypto_combobox.get().strip()  # Убирает лишние пробелы в выбраном коде криптовалюты из словаря (при их наличии)
    if crypto_code:  # Если любой код из выпадающего списка выбран
        try:  # Пробуем выполнить запрос
            symbol = f'{crypto_code}USDT'  # Формируем название торговой пары  понятное выбранному сайту
            response = requests.get(f'https://api.binance.com/api/v3/ticker/price',
                                    params={"symbol": symbol})  # ОТправляем запрос на сайт с выбранной парой
            response.raise_for_status()  # Проверяем что сервер ответил, а не выдал ошибку
            data = response.json()  # Проверащаем ответ сервера JSON в ckjdfhm Python
            exchange_price = float(data['price'])  # Достаем цену с сайта и превращаем строку в нецелочисленное число
            crypto = crypto_currencies[crypto_code]  # Находим в словаре полное название для подписи криптовалюты
            change_label.config (text = (f'Курс: {exchange_price:.2f} USD за 1 {crypto}'))  # Показвает в главном окне курс обмена (2 знака после запятой)
        except Exception as er:  # На случай ошибки, отсутствия интернета, неверной пары и т.д.
            mb.showerror('Ошибка', er)  # Покажет окно с ошибкой

    else:  # Сработает если пользователь не выбрал из выпадабщего списка криптовалюту и нажмет кнопку
        mb.showwarning('Внимание', 'Выберите криптовалюту')  # Покажет окно с ошибкой и подсказкой


def exchange_all():  # Функция вызывается при нажатии на кнопку
    crypto_code = crypto_combobox.get().strip()  # Убирает лишние пробелы в выбраном коде криптовалюты из словаря (при их наличии)
    try:  # Пробуем выполнить запрос
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price')  # ОТправляем запрос на сайт с выбранной парой
        response.raise_for_status()  # Проверяем что сервер ответил, а не выдал ошибку

        window_all = Toplevel(root)  # Создаем новое окно поверх окна root
        window_all.withdraw()
        window_all.title('Все курсы криптовалют к USD')  # Подписываем имя нового окна
        root.update_idletasks()  # обновляем геометрию главного окна, чтобы знать его точные размеры
        new_w, new_h = 400, 600

        # Координаты и размеры главного окна
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_w = root.winfo_width()
        main_h = root.winfo_height()

        # Справа от главного, с отступом 10 px
        new_x = main_x + main_w + 10

        # По вертикали — центры совпадают
        center_y = main_y + main_h // 2
        new_y = center_y - new_h // 2

        window_all.geometry(f'{new_w}x{new_h}+{new_x}+{new_y}')
        rates_label = Label(window_all, text='Загрузка...',
                            font=("SegoeUI", 12), justify=LEFT)
        rates_label.pack(pady=10, padx=10)

        def refresh_rates():  # Функция обновления курсов в реальном времени
            if not window_all.winfo_exists():  # Если окно закрыто — прекращаем обновление
                return

            try:
                resp = requests.get('https://api.binance.com/api/v3/ticker/price')  # Запрос цен всех пар
                resp.raise_for_status()  # Проверяем, что сервер ответил
                data = resp.json()  # Превращаем ответ в словарь
                prices = {item['symbol']: item['price'] for item in data}  # Собираем пары «символ — цена»
                lines = []
                for code, name in crypto_currencies.items():
                    symbol = f'{code}USDT'
                    if symbol in prices:
                        r = float(prices[symbol])
                        lines.append(f'{name} ({code}): {r:.2f} USD\n')
                    else:
                        lines.append(f'{name} ({code}): пара не найдена')

                rates_label.config(text='\n'.join(lines))  # ОБНОВЛЯЕМ текст, а не создаём новый Label
            except Exception as er:
                    rates_label.config(text=f'Ошибка обновления: {er}')

            window_all.after(5000, refresh_rates)  # следующее обновление через 5 секунд

        refresh_rates()

        Button(window_all, text='Закрыть',
                   command=window_all.destroy).pack(pady=8)
        window_all.deiconify()

    except Exception as er:
        mb.showerror('Ошибка', er)

crypto_currencies = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binancecoin',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
    'TRX': 'TRON',
    'LTC': 'Litecoin',
    'LINK': 'Chainlink',
    'AVAX': 'Avalanche',
    'SHIB': 'Shiba Inu',
    'UNI': 'Uniswap',
    'ATOM': 'Cosmos',
    'ETC': 'Ethereum Classic',
}  # Словарь ключ короткий code криптовалюты, значение полное название


root = Tk()  # Создаем главное окно приложения
root.title('Курс обмена криптовалют к USD')  # СОздаем заголовок окна
center_window(root,360, 300)  # Устанавлеваем размеры окна в пикселях

Label(root, text='Выберите криптовалюту', font=("SegoeUI", 14)).pack(pady=5)  # pady отступ сверху
crypto_combobox = ttk.Combobox(root, values=list(crypto_currencies.keys()))  # Создаем виджет с выпадающим списком криптовалют
crypto_combobox.pack(pady=3, padx=10)  # Размещаем виджет в созданном окне
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)  # Привязываем действие при выборе криптовалюты


crypto_label = ttk.Label(font=("SegoeUI", 10))  # Создаем пустое место для дальнейшего размещения там полного названия криптовалюты
crypto_label.pack()  # Размещаем это пустое место в окне


change_label = ttk.Label(font=("SegoeUI", 14))  # Создаем пустое место для дальнейшего размещения там запрашиваемого курса криптовалюты
change_label.pack(pady=10)  # Размещаем это пустое место в окне


Button(text='Получить курс выбраной валюты к USD',
       command=exchange, font=("SegoeUI", 10)).pack(pady=15, padx=10)  # Создаем кнопку при нажатии вызывающую функцию exchange


Button(text='Получить текущий курс всех валют к USD',
       command=exchange_all, font=("SegoeUI", 10)).pack(pady=15, padx=10)  # Создаем кнопку при нажатии вызывающую функцию exchange
root.mainloop()  # Запускаем главный цикл - окно остается открытым и реагирует на действия
