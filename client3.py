################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request
import time

QUERY = "http://localhost:8080/query?id={}".format(random.random())

def getDataPoint(quote):
    """ Produce all of the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Avoid division by zero
    return price_a / price_b

def main():
    """ Main entry point for the client. """
    # Query the price once every N seconds.
    N = 60
    prices = {}

    while True:
        quotes = json.loads(urllib.request.urlopen(QUERY).read())
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price
            print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")

        # Assuming we are comparing the first two stocks in the quotes list
        stock_names = list(prices.keys())
        if len(stock_names) >= 2:
            ratio = getRatio(prices[stock_names[0]], prices[stock_names[1]])
            print(f"Ratio {stock_names[0]}/{stock_names[1]} = {ratio}")
        else:
            print("Not enough stock data to compute the ratio.")

        time.sleep(N)

if __name__ == "__main__":
    main()
`
