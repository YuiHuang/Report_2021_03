import os
import pandas as pd

def fcst_EPS(ticker, year, season, year_m, month):
    """ 預測EPS
    #=== ticker: 股票代碼
    #=== year: 財務季報的年度
    #=== season: 財務季報的季度
    #=== year_m: 月營收的截止年度
    #=== month: 月營收的截止月份
    """
    #=== 最近3個月的名稱
    three_months = []
    y = int(year_m)
    m = int(month)
    three_months_pre = []
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

    # 讀入歷史季報資料
    fn = f"../data/fs_report/fs_{ticker}_20184.csv"
    df = pd.read_csv(fn, encoding="utf-8", index_col=0)
    df = df.T

    #=== 最近4季的季度名稱
    four_seasons = [year + season]
    y = int(year)
    s = int(season)
    four_seasons_pre = [str(y-1) + season]
    while len(four_seasons) < 4:
        s -= 1
        if s == 0:
            s = 4
            y -= 1
        four_seasons.append(str(y) + str(s))
        four_seasons_pre.append(str(y-1) + str(s))
    four_seasons.reverse()
    four_seasons_pre.reverse()

    #=== 最近4季的EPS & 利益率
    EPS = 0
    gm4 = [] #gross margin (毛利)
    opm4 = [] # operating margin (營業利益率)
    cap = 0
    cap_pre = 0
    for i in range(4):
        EPS += df.loc[four_seasons[i], "基本每股盈餘（元）"]
        gm4.append(df.loc[four_seasons[i], "毛利率"])
        opm4.append(df.loc[four_seasons[i], "營業利益率"])
        cap += df.loc[four_seasons[i], "股本"]
        cap_pre += df.loc[four_seasons_pre[i], "股本"]

    #=== 年增率
    gm_yoy = (sum(gm4[1:]) / 3 - gm4[0]) / gm4[0]
    opm_yoy = (sum(opm4[1:]) / 3 - opm4[0]) / opm4[0]
    cap /= 4
    cap_pre /= 4
    cap_yoy = (cap - cap_pre) / cap_pre

    EPS_new = EPS * (1 + rev3_yoy) * min((1 + gm_yoy), (1 + opm_yoy)) / (1 + cap_yoy)

    print(f"{year_m} 年 {month} 月")
    print(f"近4季的EPS: {EPS:.2f}")
    print(f"最近3個月的營收YoY (%): {rev3_yoy * 100:.1f}")
    print(f"毛利率YoY (%): {gm_yoy * 100:.1f}")
    print(f"營業利益率YoY (%): {opm_yoy * 100:.1f}")
    print(f"股本YoY (%): {cap_yoy * 100:.1f}")
    print(f"EPS預測值: {EPS_new:.2f}")

    return EPS_new

if __name__ == '__main__':
    os.system('clear')
    period = [("2019", "1", "2019", "5"),
              ("2019", "2", "2019", "8"),
              ("2019", "3", "2019", "11"),
              ("2019", "4", "2020", "3"),
              ("2020", "1", "2020", "5"),
              ("2020", "2", "2020", "8"),
              ("2020", "3", "2020", "11")]
    """
    period = [("2016", "1", "2016", "5"),
              ("2016", "2", "2016", "8"),
              ("2016", "3", "2016", "11"),]
    """
    for (year, season, year_m, month) in period:
        print(f"*** {year_m} 年 {month} 月")
        EPS_new = fcst_EPS("4205", year, season, year_m, month)
        print(f"*** EPS預測值: {EPS_new:.2f}")