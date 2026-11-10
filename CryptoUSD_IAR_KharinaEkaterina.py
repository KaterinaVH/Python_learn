from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk  # Импортируем виджеты (нам нужна для создания выпадающего списка)
import requests  # Импортируем библиотеку для работы с запросами в интернет (API, JSON)


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
            exchange_rate = float(data['price'])  # Достаем цену с сайта и превращаем строку в нецелочисленное число
            crypto = crypto_currencies[crypto_code]  # Находим в словаре полное название для подписи криптовалюты
            mb.showinfo('Текущий курс обмена',
                            f'Курс: {exchange_rate:.2f} USD за 1 {crypto}')  # Показваем окно с курсом (2 знака после запятой)
        except Exception as er:  # На случай ошибки, отсутствия интернета, неверной пары и т.д.
            mb.showerror('Ошибка', er)  # Покажет окно с ошибкой

    else:  # Сработает если пользователь не выбрал из выпадабщего списка криптовалюту и нажмет кнопку
        mb.showwarning('Внимание', 'Выберите криптовалюту')  # Покажет окно с ошибкой и подсказкой


crypto_currencies = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'SOL': 'Solana',
    'BNB': 'Binancecoin',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
}  # Словарь ключ короткий code криптовалюты, значение полное название


root = Tk()  # Создаем главное окно приложения
root.title('Курс обмена криптовалют к USD')  # СОздаем заголовок окна
root.geometry('360x200')  # Устанавлеваем размеры окна в пикселях

Label(root, text='Выберите криптовалюту').pack(pady=5)  # pady отступ сверху
crypto_combobox = ttk.Combobox(root, values=list(crypto_currencies.keys()))  # Создаем виджет с выпадающим списком криптовалют
crypto_combobox.pack(pady=3, padx=10)  # Размещаем виджет в созданном окне
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)  # Привязываем действие при выборе криптовалюты


crypto_label = ttk.Label()  # Создаем пустое место для дальнейшего размещения там полного названия криптовалюты
crypto_label.pack()  # Размещаем это пустое место в окне


Button(text='Получить текущий курс к USD',
       command=exchange).pack(pady=15, padx=10)  # Создаем кнопку при нажатии вызывающую функцию exchange


root.mainloop()  # Запускаем главный цикл - окно остается открытым и реагирует на действия
