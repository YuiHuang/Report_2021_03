import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

def plot_two_axes(ticker, df, yLabel1, yLabel2):
    """繪製雙軸線圖
    #=== ticker: 股票代碼
    #=== df: pandas DataFrame
    #=== yLabel1: 左邊Y軸的資料來源
    #=== yLabel2: 右邊Y軸的資料來源
    """
    ax1 = df[yLabel1].plot(color="blue")
    ax1.set_ylabel(f"{yLabel1} (藍線)")
    ax1.set_ylim(ymin=0)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df[yLabel2].plot(ax=ax2, color="red")
    ax2.set_ylabel(f"{yLabel2} (紅線)")
    ax2.set_ylim(ymin=0)
    ax1.set_xlabel("年度 + 季度")

    df1 = df[[yLabel1, yLabel2]]

    plt.title(f"股票代碼:{ticker}, Corr={df1.corr().loc[yLabel1, yLabel2]:.2f}")
    plt.savefig(dpi=150, fname=f"../figure/corr_{ticker}_{yLabel1}.png")
    plt.show()
    plt.close()
# ======================================================================
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
        #=== 找出每月收盤價
        date = data[i].split(',"o":')[0][:-2] #yyyymm
        closing_price = float(data[i].split(',"c":')[1].split(',"v":')[0])
        price[date] = closing_price

    return price
# ======================================================================
def cal_corr(ticker, account_title, year_e, season_e):
    """計算財務指標與股票收盤價格的相關係數
    #=== ticker: 股票代碼
    #=== account_title
    #=== year_e: 截止年度
    #=== season_e: 截止季度
    """
    fn = f"../data/fs_report/fs_{ticker}_{year_e}{season_e}.csv"
    df = pd.read_csv(fn, encoding="utf-8", index_col=0)
    #=== 只使用綜合損益表
    df = df.iloc[:17]
    df = df.drop(index="淨利（淨損）歸屬於母公司業主")
    #=== 計算滾動的近4季EPS
    new_row = []
    for i in range(df.shape[1]):
        if i < 3:
            new_row.append(0)
        else:
            new_row.append(df.loc["基本每股盈餘（元）", df.columns[i]] +
                           df.loc["基本每股盈餘（元）", df.columns[i-1]] +
                           df.loc["基本每股盈餘（元）", df.columns[i-2]] +
                           df.loc["基本每股盈餘（元）", df.columns[i-3]])
    df2 = pd.DataFrame([new_row], columns=df.columns, index=["近4季EPS"])
    df = df.append(df2)
    df = df.drop(columns=[df.columns[0], df.columns[1], df.columns[2]])
    df = df.T
    #=== 爬網取得每個月的股價資訊
    price = get_Yahoo_stock_price(ticker)
    new_col = []
    for season in df.index:
        month = int(season[-1]) * 3
        year = int(season[:-1])
        if month > 12:
            year += 1
            month -= 12
        elif month <= 0:
            year -= 1
            month += 12

        month = str(year) + f"{month:02d}"
        new_col.append(price[month])
    df["收盤價"] = new_col
    #=== 繪製雙軸線圖
    plot_two_axes(ticker, df, account_title, "收盤價")
    #=== 計算各項財務指標與股價的相關係數
    corr = df.corr()
    corr = corr.reindex(corr["收盤價"].abs().sort_values(ascending=False).index)
    corr[["收盤價"]].to_excel(f"{ticker}_財務指標與股價的相關係數.xlsx", encoding="utf-8")
# ======================================================================
if __name__ == "__main__":
    os.system("clear")
    cal_corr("4205", "近4季EPS", "2020", "3")