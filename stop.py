import asyncio
import tkinter as tk

# from functools import partial

from binance.client import AsyncClient
from binance.exceptions import BinanceAPIException
import os
import subprocess

from tkinter import messagebox

def cancel():
    subprocess.Popen(["python", "cancel.py"])



async def get_trailing_stop_orders(symbols, root, client):

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
                label_text = f"Тип: {order['type']}\nЦена активации: {order['activatePrice']}\nЛот: {order['origQty']}\nСимвол: {symbol}\nСторона: {order['side']}"
                
                button = tk.Button(
                    root, 
                    text="Отменить", 
                    # command=lambda symbol=symbol, order_id=order['orderId']: asyncio.create_task(cancel_order(client, symbol, order_id)))
                    command=cancel
                )

                label = tk.Label(root, text=label_text, anchor='w', justify='left')
                label.pack()

                
                button.configure(background="brown", foreground="white")
                button.pack()
                # print(order_info)
                print(f"НАЙДЕН БОТ ДЛЯ ВАЛЮТНОЙ ПАРЫ {symbol}: {order} \n")
        # else:
        #     print(f"Не найден бот для валютной пары: {symbol}")
        
        # await client.close_connection()


async def cancel_order(client, symbol, order_id):
    # Replace with your Binance API key and secret
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')
    
    # Create a new client instance for canceling the order
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    
    try:
        # Cancel the trailing stop loss order
        await client.futures_cancel_order(symbol=symbol, origClientOrderId=order_id)
        # button.config(state=tk.DISABLED)
        print(f"Cancelled order: {order_id}")
        messagebox.showinfo("Ставка отменена!")
    except BinanceAPIException as e:
        print(f"Failed to cancel order: {order_id}. Error: {e}")
    finally:
        await client.close_connection()
   

async def main():
    # Replace with your Binance API key and secret
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')

    # create AsyncClient
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)

    # Define your list of symbols
    symbols = ['SOLUSDT', 'XLMUSDT', 'DOGEUSDT', 'ADAUSDT', 'LINKUSDT','XRPUSDT','NEOUSDT',"1000SHIBUSDT", "AVAXUSDT"]

    # Create the Tkinter window
    root = tk.Tk()

    # Call the function to run the trailing stop orders
    await get_trailing_stop_orders(symbols, root, client)

    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")

    # Run the Tkinter event loop
    root.mainloop()

    # Close the client session
    await client.close_connection()

# Run the main function
asyncio.run(main())