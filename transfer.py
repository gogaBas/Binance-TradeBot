import tkinter as tk
import asyncio
from binance import AsyncClient
import os
from tkinter import messagebox


# Binance API key and secret
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

# Create the Tkinter window
root = tk.Tk()
root.title("Сумма в кошелёк")

label = tk.Label(root, text="Сумма для перевода $:")
label.pack()

root.geometry("200x100")

# Create a PRICE Spinbox widget with a range of values
amount = tk.Spinbox(root, from_=0, to=10000, increment=0.01, format="%.2f")
amount.pack()


#  function to get the value from the Spinbox widget
def get_spinbox_value():
    get_value = amount.get()
    print(f"Amount: {get_value}")
    return get_value




async def transfer_funds():

    # Create the Binance API client
    client = await AsyncClient.create(api_key, api_secret)

     # Get the futures account information
    futures_account = await client.futures_account()

    amount = get_spinbox_value()

    # Calculate the amount to transfer (use the available balance if amount is not specified)
    if amount is None:
        amount = float(futures_account.totalCrossWalletBalance)
        messagebox.showerror("ошибка", "Сумма не указана!", amount)
        print(f"Amount: {amount}")

    else:
        amount = float(amount)
        print(f"Amount: {amount}")
        messagebox.showinfo("Успех", "Сумма переведена!")

    # Transfer funds from futures wallet to spot account
    await client.futures_account_transfer(fromAccountType='USDT_FUTURE', toAccountType='SPOT', asset='USDT', amount=amount, type=2)

    # Close the API connection
    await client.close_connection()

def button_click():
    # Run the async function in an event loop
    # in case of error put this code after transfer_funds() function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(transfer_funds()) 

button = tk.Button(root, text="Перевести", command=button_click)
button.pack()
# Change the button color and text color
button.configure(background="green", foreground="white")
button.pack()

# Start the Tkinter event loop
root.mainloop()