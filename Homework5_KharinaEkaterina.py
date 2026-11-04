from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import json
import pprint

from bottle import response


def update_currency_label(event):
    code = target_combobox.get()
    name = currencies[code]
    target_label.config(text=name)


def update_base_label(event):
    code = base_combobox.get()
    name = currencies[code]
    base_label.config(text=name)

def update_base_label_2(event):
    code = base_combobox_2.get()
    name = currencies[code]
    base_label_2.config(text=name)


def exchange():
    target_code = target_combobox.get().strip()
    base_code = base_combobox.get().strip()
    base_code_2 = base_combobox_2.get().strip()
    if target_code and base_code and base_code_2:
        try:

            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()
            data = response.json()
            response_2 = requests.get(f'https://open.er-api.com/v6/latest/{base_code_2}')
            response_2.raise_for_status()
            data_2 = response_2.json()
            if target_code in data['rates'] and target_code in data_2['rates']:
                exchange_rate = data['rates'][target_code]
                exchange_rate_2 = data_2['rates'][target_code]
                base = currencies[base_code]
                base_2 = currencies[base_code_2]
                target = currencies[target_code]
                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:.1f} {target} за 1 {base}\n'
                            f'Курс: {exchange_rate_2:.1f} {target} за 1 {base_2}')
            else:
                mb.showerror('Ошибка',
                             f'Валюта {target_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Введите код валюты')


currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'

}

root = Tk()
root.title('Курс обмена валют USD')
root.geometry('360x280')

Label(root, text='Базовая валюта').pack()
base_combobox = ttk.Combobox(root, values=list(currencies.keys()))
base_combobox.pack(pady=3, padx=10)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)
base_label = ttk.Label()
base_label.pack()

Label(root, text='Вторая базовая валюта').pack()
base_combobox_2 = ttk.Combobox(root, values=list(currencies.keys()))
base_combobox_2.pack(pady=3, padx=10)
base_combobox_2.bind('<<ComboboxSelected>>', update_base_label_2)
base_label_2 = ttk.Label()
base_label_2.pack()

Label(root, text='Целевая валюта').pack(padx=10)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()))
target_combobox.pack(pady=3, padx=10)
target_combobox.bind('<<ComboboxSelected>>', update_currency_label)

target_label = ttk.Label()
target_label.pack()

Button(text='Получить курс обмена валюты',
       command=exchange).pack(pady=10, padx=10)

root.mainloop()
