import asyncio
from tkinter import messagebox
import os
from binance.exceptions import BinanceAPIException

from binance import AsyncClient
# from binance.enums import *



async def main():
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')

    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)

    # Define your list of symbols
    symbols = ['SOLUSDT', 'XLMUSDT', 'DOGEUSDT', 'ADAUSDT',
               'LINKUSDT', 'XRPUSDT', 'NEOUSDT', "1000SHIBUSDT", "AVAXUSDT"]
    

    # Retrieve a list of all open orders for each symbol
    for symbol in symbols:
        orders = await client.futures_get_open_orders(symbol=symbol)

        # Check if any orders are of type TRAILING_STOP_MARKET
        trailing_stop_orders = [
            order for order in orders if order['type'] == 'TRAILING_STOP_MARKET'
        ]

        if trailing_stop_orders:
            for order in trailing_stop_orders:
                # order_info = f"Order for {symbol}: {order}"
                print(f"БОТ ДЛЯ ВАЛЮТНОЙ ПАРЫ: {symbol}\n Сторона: {order['side']}\n Цена активации: {order['activatePrice']}\n Лот: {order['origQty']}\n Код ставки: {order['clientOrderId']}\n")

                # label_text = f"Тип: {order['type']}\nЦена активации: {order['activatePrice']}\nЛот: {order['origQty']}\nСимвол: {symbol}\nСторона: {order['side']}"
                # print(label_text)



                # print(order_info)

        # else:
        #     print(f"Не найден бот для валютной пары: {symbol}")
    symbolo = input("введите валютную пару для отмены ставки: ")
    ordero = input("введите код ставки для отмены: ")

    try:
    # Cancel the trailing stop loss order
        await client.futures_cancel_order(symbol=symbolo, origClientOrderId=ordero)
        print(f"Cancelled order: {order['clientOrderId']}")
        messagebox.showinfo("Ставка отменена!")
    except BinanceAPIException as e:
        print(f"Failed to cancel order: {order['clientOrderId']}. Error: {e}")
        messagebox.showerror("ошибка", "Ставка не отменена!")

    await client.close_connection()

asyncio.run(main())
