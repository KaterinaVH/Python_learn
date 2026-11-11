"""
Приложение «Курс криптовалют».

Показывает курс выбранной криптовалюты к USDT (≈ USD) и список всех курсов
в отдельном окне. Данные берутся с публичного API Binance.
"""

import customtkinter as ctk  # Импортирует библиотеку для красивого и современного окна
from tkinter import messagebox as mb  # Импортируем вспомогательные окна
import requests  # Импортируем библиотеку для работы с запросами в интернет (API, JSON)

ctk.set_appearance_mode("dark")  # тёмная тема
ctk.set_default_color_theme("green")  # Делает акцент выбранного цвета для кнопок и полей


"""
Показывает полное название криптовалюты при выборе ее из выпадающего списка
"""


def update_crypto_label(event):
    code = crypto_combobox.get()  # Получаем выбранный код криптовалюты
    name = crypto_currencies[code]  # По коду находим полное название криптовалюты
    crypto_label.configure(text=name)  # Подписываем название криптовалюты под списком


"""
Запрашивает куры выбранной криптовалюты к USDT(обозначение USD на сайте) и выводит его в главное окно
"""


def exchange():  # Функция вызывается при нажатии на кнопку
    crypto_code = crypto_combobox.get().strip()  # Убирает лишние пробелы в выбраном коде криптовалюты из словаря (при их наличии)
    if crypto_code:  # Если любой код из выпадающего списка выбран
        try:  # Пробуем выполнить запрос
            symbol = f'{crypto_code}USDT'  # Формируем название торговой пары  понятное выбранному сайту
            response = requests.get(f'https://api.binance.com/api/v3/ticker/price',
                                    params={"symbol": symbol})  # Отправляем запрос на сайт с выбранной парой
            response.raise_for_status()  # Проверяем что сервер ответил, а не выдал ошибку
            data = response.json()  # Проверащаем ответ сервера JSON в словарь Python
            exchange_price = float(data['price'])  # Достаем цену с сайта и превращаем строку в нецелочисленное число
            crypto = crypto_currencies[crypto_code]  # Находим в словаре полное название для подписи криптовалюты
            change_label.configure(text=(f'Курс: {exchange_price:.2f} USD за 1 {crypto}'),
                                   font=('Consolas', 20))  # Показвает в главном окне курс обмена (2 знака после запятой)
        except Exception as er:  # На случай ошибки, отсутствия интернета, неверной пары и т.д.
            mb.showerror('Ошибка', er)  # Покажет окно с ошибкой

    else:  # Сработает если пользователь не выбрал из выпадабщего списка криптовалюту и нажмет кнопку
        mb.showwarning('Внимание', 'Выберите криптовалюту')  # Покажет окно с ошибкой и подсказкой


"""
Открывает окно со всеми курсами и обновляет их каждые 5 секунд
"""


def exchange_all():  # Функция вызывается при нажатии на кнопку
    try:  # Пробуем выполнить запрос
        response = requests.get(
            f'https://api.binance.com/api/v3/ticker/price')  # Отправляем запрос на сайт с выбранной парой
        response.raise_for_status()  # Проверяем что сервер ответил, а не выдал ошибку

        window_all = ctk.CTkToplevel(root)  # Создаем новое окно поверх окна root
        window_all.withdraw()  # Скрываем вызванное окно пока идет настройка
        window_all.title('Все курсы криптовалют к USD')  # Подписываем имя нового окна

        root.update_idletasks()  # Пересчитывае размер главного окна
        main_x = root.winfo_x()  # Узнаем левый край главного окна (root)
        main_y = root.winfo_y()  # Узнаем верхний край главного окна (root)
        main_w = root.winfo_width()  # Узнаем ширину главного окна (root)
        main_h = root.winfo_height()  # Узнаем  высоту главного окна (root)

        new_x = main_x + main_w + 10  # Ставим второе окно справа от главного
        new_y = main_y  # Делаем так чтобы верх окон был на одной линии
        window_all.geometry(f'420x620+{new_x}+{new_y}')  # Применяем размер и позицию нового окна

        title = ctk.CTkLabel(window_all, text='Курсы криптовалют',
                             font=('Consolas', 18, 'bold'))  # Создаем заголовок внутри второг окна
        title.pack(pady=(20, 10))  # Размещаем заголовок с отступами вверху и внизу

        rates_label = ctk.CTkLabel(window_all, text='Загрузка...',
                                   font=('Consolas', 12),
                                   justify='left',
                                   anchor='w')  # Создаем подпись для списка курсов(на случай долгой загрузки)
        rates_label.pack(fill='both', expand=True, padx=20, pady=10)  # Растягиваем подпись на все окно

        """
        Обновляет список курсов и планирует следующее обновление через 5 секунд
        """

        def refresh_rates():  # Функция обновляет курсы каждые 5 секунд
            if not window_all.winfo_exists():  # Если окно закрыто — прекращаем обновление
                return

            try:
                resp = requests.get('https://api.binance.com/api/v3/ticker/price')  # Запрос цен всех пар
                resp.raise_for_status()  # Проверяем, что сервер ответил
                data = resp.json()  # Превращаем ответ в словарь
                prices = {item['symbol']: item['price'] for item in data}  # Собираем в словарь пары «символ — цена»
                lines = []  # Создаем пустой список для дальнейшей подстановки туда списка курсов всех криптовалют
                for code, name in crypto_currencies.items():  # Проходим по каждой криптовалюте из нашего словаря
                    symbol = f'{code}USDT'  # Формируем пару криптовалюта/USD понятная сайту
                    if symbol in prices:  # Если такая прара есть на сайте
                        r = float(prices[symbol])  # Достаем цену и превращаем ее в число
                        lines.append(f'{name:<16} {code:<5} {r:.2f} USD\n')  # Добавляем строку с курсом
                    else:  # Сработает если пары нет
                        lines.append(
                            f'{name} ({code}): данные по запрашиваемой криптовалюте не найдены')  # Показвает текст ошибки

                rates_label.configure(text='\n'.join(lines), font=('Consolas', 14))  # Собирает список строк из словаря криптовалют и их стоимости и обновляет текст
            except Exception as er:  # Если вдруг ошибка при обновлении
                rates_label.configure(text=f'Ошибка обновления криптовалюты: {er}')  # Показывает ошибку

            window_all.after(5000, refresh_rates)  # следующее обновление через 5 секунд

        refresh_rates()  # Запускаем сразу первое обновление

        close_btn = ctk.CTkButton(window_all, text='Закрыть',
                                  command=window_all.destroy,
                                  font=('Consolas', 12, 'bold'),
                                  fg_color='#e74c3c', hover_color='#c0392b',
                                  corner_radius=8, height=40)  # Создаем кнопку Закрыть во втором окне
        close_btn.pack(pady=20)  # Размещаем кнопку с отсупом

        window_all.deiconify()  # Показываем заполненное окно

    except Exception as er:  # Если будет ошибка при создании окна
        mb.showerror('Ошибка', er)  # Показваем уведомление об ошибке


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

root = ctk.CTk()  # Создает главное окно приложения
root.title('Курс криптовалют')  # Прописываем заголовок окна
root.geometry('400x480')  # Сначала задаём размер


title = ctk.CTkLabel(root, text='Курс криптовалют',
                     font=('Consolas', 22, 'bold'))  # Создаем крупный заголовок в главном окне
title.pack(pady=(25, 15))  # Размещаем заголовок с отступом

ctk.CTkLabel(root, text='Выберите криптовалюту',
             font=('Consolas', 14)).pack(anchor='w', padx=30)  # Создаем подпись под окном выбора криптовалюты

crypto_combobox = ctk.CTkComboBox(root, values=list(crypto_currencies.keys()),
                                  font=('Consolas', 18),
                                  dropdown_font=('Consolas', 16),
                                  state='readonly')  # Создаем выпадающий список с криптовалютами из словаря
crypto_combobox.pack(fill='x', padx=30, pady=(5, 8))  # Растгиваем список по ширине с отступами
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)  # Вышывает функцию при выборе криптовалюты

crypto_label = ctk.CTkLabel(root, text='', font=('Consolas', 12, 'italic'),
                            text_color='gray')  # Создаем пустое пространство для подписи курса криптовалюты
crypto_label.pack(pady=(0, 10))  # Размещаем подпись в главном окне

change_label = ctk.CTkLabel(root, text='—', font=('Consolas', 32, 'bold'),
                            text_color='#2ecc71')  # Создаем крупный зеленый прочерк который отображается пока не выбрали криптовалюту
change_label.pack(pady=(10, 0))  # Размещаем подпись

change_sub_label = ctk.CTkLabel(root, text='', font=('Consolas', 11),
                                text_color='gray')  # Создаем место для подписикурса криптовалюты за 1 USD
change_sub_label.pack(pady=(0, 20))  # Размещаем подпись

btn1 = ctk.CTkButton(root, text='Курс выбранной валюты',
                     command=exchange,
                     font=('Consolas', 15, 'bold'),
                     corner_radius=10, height=45)  # Кнопка получить курс
btn1.pack(fill='x', padx=30, pady=(5, 10))  # Растягиваем кнопку по ширинк

btn2 = ctk.CTkButton(root, text='Все курсы криптовалют',
                     command=exchange_all,
                     font=('Consolas', 15, 'bold'),
                     fg_color='#27ae60', hover_color='#1e8449',
                     corner_radius=10, height=45)  # Вторя кнопка Все курсы криптовалют
btn2.pack(fill='x', padx=30, pady=(0, 25))  # Растягиваем кнопку по ширине

root.mainloop()  # Запускаем главный цикл
