import os
import pandas as pd
import numpy as np
from scipy import stats

def fcst_EPS(ticker, year, season, year_m, month):
    """ 預測EPS
    #=== ticker: 股票代碼
    #=== year: 財務季報的年度
    #=== season: 財務季報的季度
    #=== year_m: 月營收的截止年度
    #=== month: 月營收的截止月份
    """
    fn = f"../data/fs_report/fs_{ticker}_20184.csv"
    df = pd.read_csv(fn, encoding="utf-8", index_col=0)
    df = df.T
    #=== 股本的年增率
    cap = df.loc[year + season, "股本"]
    cap_pre = df.loc[str(int(year)-1) + season, "股本"]
    cap_yoy = (cap - cap_pre) / cap_pre

    #=== 最近4季的季度名稱
    four_seasons = [year + season]
    y = int(year)
    s = int(season)
    while len(four_seasons) < 4:
        s -= 1
        if s == 0:
            s = 4
            y -= 1
        four_seasons.append(str(y) + str(s))

    #=== 最近4季的EPS & 營業利益率
    EPS4 = 0
    margin4 = []
    for i in range(4):
        EPS4 += df.loc[four_seasons[i], "基本每股盈餘（元）"]
        margin4.append(df.loc[four_seasons[i], "營業利益率"])
    margin4.reverse()
    print("近4季的EPS:", EPS4)

    #=== 最近3個月的名稱
    three_months = [year_m + month]
    y = int(year_m)
    m = int(month)
    three_months_pre = [str(y-1) + month]
    while len(three_months) < 3:
        m -= 1
        if m == 0:
            m = 12
            y -= 1
        three_months.append(str(y) + str(m))
        three_months_pre.append(str(y-1) + str(m))

    #=== 最近3個月的營收的年增率
    rev3 = 0
    rev3_pre = 0
    for i in range(3):
        fn = f"../data/mth_revenue/rev_{three_months[i]}.csv"
        df = pd.read_csv(fn, encoding="utf-8", index_col="公司代號")
        rev3 += df.loc[int(ticker), "月營收"]
        fn = f"../data/mth_revenue/rev_{three_months_pre[i]}.csv"
        df = pd.read_csv(fn, encoding="utf-8", index_col="公司代號")
        rev3_pre += df.loc[int(ticker), "月營收"]
    rev3_yoy = (rev3 - rev3_pre) / rev3_pre
    print(f"最近3個月的營收YoY (%): {rev3_yoy * 100:.1f}")

    #=== 利益率年增率
    x = np.arange(0, 4)
    y = np.array(margin4)
    res = stats.linregress(x, y)
    if res.slope > 0:
        margin_yoy = np.percentile(y, 75) - np.percentile(y, 50)
    elif res.slope < 0:
        margin_yoy = np.percentile(y, 25) - np.percentile(y, 50)
    else:
        margin_yoy = 0
    margin_yoy /= np.percentile(y, 50)
    print("營業利益率YoY (%): {margin_yoy * 100:.1f}")
    print(f"股本YoY (%): {cap_yoy * 100:.1f}")
    EPS_new = EPS4 * (1 + rev3_yoy) * (1 + margin_yoy) / (1 + cap_yoy)
    print(f"EPS預測值: {EPS_new:.2f}")





if __name__ == '__main__':
    os.system('clear')
    year = "2016"
    season = "3"
    year_m = "2016"
    month = "11"
    fcst_EPS("2330", year, season, year_m, month)