import asyncio
import tkinter as tk

import subprocess

from tkinter import messagebox

from binance import AsyncClient
from binance.enums import *
import os
import json

# Replace with your Binance API key and secret
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')


# FUNCTIONS here


def bet_size():
    string_value = spinbox.get()

    print("Значение лота:", int(string_value))
    # print("Text value:", text_value)
    return string_value


def currency_pair():  # options dropdown menu
    selected_option = option_var.get()
    print("выбранная пара:", selected_option)
    return selected_option


def bet_side():  # radio buttons
    selected_value = radio_var.get()
    print("выбранная позиция:", selected_value)
    return selected_value


def activation_price():
    string_value = price.get()
    print("Цена активации:", string_value)
    return string_value

def callbackRate():
    string_value = callback_percent.get()
    print("процент колебания ставки:", string_value)
    return string_value

def run_other_program():
    subprocess.Popen(["pythonw", "stop.py"])

def run_transfer():
    subprocess.Popen(["pythonw", "transfer.py"])

# running tkinter
root = tk.Tk()

# title of the window
root.title("КРИПТО-БОТ")

# window size
root.geometry("250x350")
# window icon
root.iconbitmap("icon.ico")

run_other_program()


# button running in new window
transfer = tk.Button(root, text="Перевести в кошелёк", command=run_transfer)
transfer.pack()

# button running in new window
button = tk.Button(root, text="Открыть активные боты", command=run_other_program)

button.pack()

# Create a label for the text input field
text_label = tk.Label(root, text="валютная пара, пример: xlmusdt:")
text_label.pack()

# Create a list of options
options = ["xlmusdt", "dogeusdt", "adausdt", "linkusdt",
           "xrpusdt", "neousdt", "1000shibusdt", "avaxusdt"]

# Create a variable to store the currency pair
option_var = tk.StringVar(root)
# # Set the default selected option
# option_var.set(options[0])

# Create the dropdown menu
option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.config(width=15)
option_menu.pack()

# Create a button to print the currency pair
# button = tk.Button(root, text="Напечатать выбранный вариант", command=currency_pair)
# button.pack()

# Create a variable to store the selected radio button value
radio_var = tk.StringVar()

# Create radio buttons for bet side
radio_button1 = tk.Radiobutton(
    root, text="Покупка", variable=radio_var, value="BUY")
radio_button1.pack()

radio_button2 = tk.Radiobutton(
    root, text="Продажа", variable=radio_var, value="SELL")
radio_button2.pack()


# Set the value of radio_var to select the second radio button
radio_var.set("BUY")

# Create a button to show the selected value
# button = tk.Button(root, text="Показать выбранное", command=bet_side)
# button.pack()


# Create a label for the text input field for the bet size
text_label = tk.Label(root, text="Размер лота:")
text_label.pack()

# Create a Spinbox widget with a range of values
spinbox = tk.Spinbox(root, from_=0, to=10000, increment=10)
spinbox.pack()

# Create a button to print the values of bet size
# button = tk.Button(root, text="Напечатать значения", command=bet_size)
# button.pack()

# Create a label for the text input field for the bet size
text_label = tk.Label(root, text="цена активации бота:")
text_label.pack()

# Create a PRICE Spinbox widget with a range of values
price = tk.Spinbox(root, from_=0, to=100, increment=0.01)
price.pack()

# label for callback rate of a bet
text_label = tk.Label(root, text="процент колебания ставки:")
text_label.pack()

# Create a callback rate Spinbox widget with a range of values
callback_percent = tk.Spinbox(root, from_=0.1, to=5, increment=0.1)
callback_percent.pack()

# Create a button to print the values of activation price
# button = tk.Button(root, text="Напечатать значения", command=callbackRate)
# button.pack()


# Define an async function
async def async_function():
    # Create the Binance async client
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)

    # defining the symbol as tkinter variables
    symbol = currency_pair()
    symbol = symbol.upper()
    print(symbol)

    side = bet_side()
    side = side.upper()
    print(side)

    quantity = bet_size()
    quantity = int(quantity)
    print(quantity)

    act_price = activation_price()
    act_price = float(act_price)
    print(act_price)

    # Define the parameters for the trailing stop loss order, such as callbackRate
    # callback_rate = 0.1
    callback_rate = callbackRate()

    # Create the trailing stop loss order
    order = await client.futures_create_order(
        symbol=symbol,
        side=side,  # Replace with the desired side (SELL or BUY)
        type="TRAILING_STOP_MARKET",
        quantity=quantity,
        activationPrice=act_price,
        callbackRate=callback_rate
    )
    # make order readable
    order = json.dumps(order, indent=4)  # may case error
    print(f"order variable type is: {type(order)} \n order details: {order}")

    if order:
        print(
            f"{order}\n"
            "ходящий стоп поставлен\n"
            # "код этого стопа: "
            # f"{order['clientOrderId']}"
        )
        messagebox.showinfo("Успех", "Ставка создана!")
        print(" Ставка не создана")
    else:
        messagebox.showerror("ошибка", "Ставка не создана!")

    # Close the client connection
    await client.close_connection()


# Define a callback function for a button
def button_callback():
    # Run the async function in an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_function())


# Add a button to the window
button = tk.Button(root, text="Запустить бот", command=button_callback)
# Change the button color and text color
button.configure(background="purple", foreground="white")
button.pack()

# Start the Tkinter event loop
root.mainloop()
