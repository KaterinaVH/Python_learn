from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


def update_currency_label(event):
    code = target_combobox.get()
    name = currencies[code]
    target_label.config(text=name)


def update_crypto_label(event):
    code = crypto_combobox.get()
    name = currencies[code]
    crypto_label.config(text=name)


def exchange():
    target_code = target_combobox.get().strip()
    crypto_code = crypto_combobox.get().strip()
    if target_code and crypto_code:
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price',
                                    params={"ids": crypto_code, "vs_currencies": target_code.lower()})
            response.raise_for_status()
            data = response.json()
            if crypto_code in data and target_code.lower() in data[crypto_code]:
                exchange_rate = data[crypto_code][target_code.lower()]
                crypto = currencies[crypto_code]
                target = currencies[target_code]
                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:.1f} {target} за 1 {crypto}')
            else:
                mb.showerror('Ошибка',
                             f'Валюта {target_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Введите код валюты')


currencies = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'SOL': 'Solana',
    'BNB': 'Binancecoin',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
}

coingecko_ids = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'SOL': 'Solana',
    'BNB': 'Binancecoin',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
}

root = Tk()
root.title('Курс обмена криптовалют USD')
root.geometry('360x280')

Label(root, text='Крипто валюта').pack()
crypto_combobox = ttk.Combobox(root, values=list(currencies.keys()))
crypto_combobox.pack(pady=3, padx=10)
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)
crypto_label = ttk.Label()
crypto_label.pack()

Label(root, text='Целевая валюта').pack(padx=10)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()))
target_combobox.pack(pady=3, padx=10)
target_combobox.bind('<<ComboboxSelected>>', update_currency_label)

target_label = ttk.Label()
target_label.pack()

Button(text='Получить курс обмена валюты',
       command=exchange).pack(pady=10, padx=10)

root.mainloop()
