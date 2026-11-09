from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


def update_crypto_label(event):
    code = crypto_combobox.get()
    name = currencies[code]
    crypto_label.config(text=name)


def exchange():
    crypto_code = crypto_combobox.get().strip()
    if crypto_code:
        try:
            crypto_id = coingecko_ids[crypto_code]
            response = requests.get('https://api.coingecko.com/api/v3/simple/price',
                                    params={"ids": crypto_id, "vs_currencies": "USD"})
            response.raise_for_status()
            data = response.json()
            if crypto_id in data and "usd" in data[crypto_id]:
                exchange_rate = data[crypto_id]["usd"]
                crypto = currencies[crypto_code]
                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:.2f} USD за 1 {crypto}')
            else:
                mb.showerror('Ошибка',
                             f'Курс для {crypto_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Выберите криптовалюту')


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
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'DOGE': 'dogecoin',
    'DOT': 'polkadot',
}

root = Tk()
root.title('Курс криптовалют к USD')
root.geometry('360x140')

Label(root, text='Криптовалюта').pack()
crypto_combobox = ttk.Combobox(root, values=list(currencies.keys()))
crypto_combobox.pack(pady=3, padx=10)
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)
crypto_label = ttk.Label()
crypto_label.pack()

Button(text='Получить курс к USD',
       command=exchange).pack(pady=10, padx=10)

root.mainloop()
