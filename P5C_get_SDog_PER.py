import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_SDog_PER(ticker, today, year):
    """ 抓取財報狗資料
    #=== ticker: 股票代碼
    #=== today: 最近一個收盤日期
    #=== year: 最新發佈的季報的年度
    """
    no_data = ['無', '虧損', '無資料', '前期為零']
    sdog_year = today[:4]
    sdog_season = str((int(today[4:6]) - 1) // 3 + 1)
    url = 'https://statementdog.com/api/v1/fundamentals/'
    url += ticker + '/'
    url += str(int(year)-5) + '/' + '1' + '/'
    url += sdog_year + '/' + sdog_season + '/'
    url += 'cf?queried_by_user=true&_=1534341070810'
    try:
        res = requests.get(url, timeout=3)
        print(f"HTTP status code: {res.status_code}")
        if res.status_code == requests.codes.ok:
            html = res.json()
        else:
            return
    except:
        print("Connection failed: SDog")
        return

    Time_M = list(np.array(html['2']['data'])[:, 1])
    PER = np.array(html['17']['data'])[:, 1]
    PER = [0 if x in no_data else float(x) for x in PER]
    text_PER = str(format(np.percentile(PER, 25), '.1f')) + ' / ' +\
        str(format(np.percentile(PER, 50), '.1f')) + ' / ' +\
        str(format(np.percentile(PER, 75), '.1f'))
    print(f"歷史本益比(PER, PR25/PR50/PR75) = {text_PER}")

    df = pd.DataFrame(index=Time_M)
    df["本益比"] = PER
    df["本益比"].plot()
    plt.title(f"股票代號:{ticker}, 歷史本益比(PR25/50/75)={text_PER}")
    plt.ylabel("本益比")
    plt.savefig(dpi=150, fname=f"../figure/{ticker}_本益比.png")
# ======================================================================
if __name__ == "__main__":
    os.system("clear")
    get_SDog_PER("2330", "20210205", "2021")