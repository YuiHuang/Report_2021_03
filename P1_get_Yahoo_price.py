import requests

def get_Yahoo_stock_price(ticker):
    """抓取Yahoo Stock的個股股價
    #=== ticker: 股票代碼
    """
    url = "https://tw.quote.finance.yahoo.net/quote/"
    url += f"q?type=ta&perd=m"
    url += f"&mkt=10&sym={ticker}"
    url += "&callback=jQuery111306117842047895292_1535895637574&_=1535895637575"

    r = requests.get(url)
    html = r.text
    print(html)
    data = html.split('{"t":')
    price = {}
    for i in range(1, len(data)):
        #=== 找出月份與對應的均價
        date = data[i].split(',"o":')[0][:-2]
        closing_price = float(data[i].split(',"c":')[1].split(',"v":')[0])
        price[date] = closing_price
    return price

if __name__ == "__main__":
    get_Yahoo_stock_price("2330")