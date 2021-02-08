import requests

def get_Yahoo_stock_price(ticker):
    """抓取Yahoo Stock的個股股價
    #=== ticker: 股票代碼
    """
    url = "https://tw.quote.finance.yahoo.net/quote/"
    url += "q?type=ta&perd=m"
    url += f"&mkt=10&sym={ticker}"
    url += "&callback=jQuery111306117842047895292_1535895637574&_=1535895637575"

    try:
        r = requests.get(url, timeout=3)
    except:
        print(f"Failed to get stock price for {ticker}")
        return "(N/A)"

    html = r.text
    data = html.split('{"t":')
    price = {}
    for i in range(1, len(data)):
        #=== 找出每月均價
        date = data[i].split(',"o":')[0][:-2]
        closing_price = float(data[i].split(',"c":')[1].split(',"v":')[0])
        price[date] = closing_price

    return price