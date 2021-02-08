import os
import pandas as pd
import numpy as np

def cal_fin_idx(ticker, year_e, season_e, duration=3):
    """匯總綜合損益表&資產負債表, 計算財務指標
    #=== ticker: 股票代碼
    #=== year_e: 截至年度
    #=== season_e: 截止季度
    #=== duration: 財報分析期間(預設3年期)
    """
    # 合併原始綜合損益表
    year_s = str(int(year_e) - duration + 1)
    fn_dst = f"../data/fs_report/fs_{ticker}_{year_e}{season_e}.csv"

    #=== 主要會計科目
    account_titles = [
        "營業收入",
        "營業毛利（毛損）",
        "營業費用",
        "營業利益（損失）",
        "營業外收入及支出",
        "稅前淨利（淨損）",
        "所得稅費用（利益）",
        "本期淨利（淨損）",
        "淨利（淨損）歸屬於母公司業主",
        "基本每股盈餘（元）",
    ]
    df = pd.DataFrame({}, index=account_titles)
    for y in range(int(year_s), int(year_e)+1):
        s_end = int(season_e) if y == int(year_e) else 4
        for s in range(1, s_end+1):
            fn = f"../data/qtr_report/is_{y}{s}.csv"
            _ = pd.read_csv(fn, encoding="utf-8", header=0, index_col="公司代號")

            new_col = {}
            for item in account_titles:
                try:
                    new_col[item] = float(_.loc[int(ticker), item])
                except:
                    new_col[item] = 0
            df_col = pd.DataFrame({str(y)+str(s): new_col})
            df = pd.concat([df, df_col], axis=1, sort=False)

    #=== 將財報原始資料中逐季累加的數字拆分成單季數字
    for i in range(df.shape[1]-1, -1, -1):
        if i % 4 != 0:
            df[df.columns[i]] = df[df.columns[i]] - df[df.columns[i-1]]

    #=== 計算各項損益比例 (%)
    FS = np.zeros((8, df.shape[1]), dtype=float)
    account_titles = [
        "毛利率",
        "營業利益率",
        "營業費用佔營收比",
        "稅前淨利率",
        "稅後淨利率",
        "業外收支佔稅前淨利比",
        "所得稅率",
        "母公司業主淨利比",
    ]
    for i in range(df.shape[1]):
        FS[0][i] = round(
            100*df.loc["營業毛利（毛損）", df.columns[i]] / df.loc["營業收入", df.columns[i]], 2)
        FS[1][i] = round(
            100*df.loc["營業利益（損失）", df.columns[i]] / df.loc["營業收入", df.columns[i]], 2)
        FS[2][i] = round(
            100*df.loc["營業費用", df.columns[i]] / df.loc["營業收入", df.columns[i]], 2)
        FS[3][i] = round(
            100*df.loc["稅前淨利（淨損）", df.columns[i]] / df.loc["營業收入", df.columns[i]], 2)
        FS[4][i] = round(
            100*df.loc["本期淨利（淨損）", df.columns[i]] / df.loc["營業收入", df.columns[i]], 2)
        FS[5][i] = round(
            100*df.loc["營業外收入及支出", df.columns[i]] / df.loc["稅前淨利（淨損）", df.columns[i]], 2)
        FS[6][i] = round(
            100*df.loc["所得稅費用（利益）", df.columns[i]] / df.loc["稅前淨利（淨損）", df.columns[i]], 2)
        FS[7][i] = round(
            100*df.loc["淨利（淨損）歸屬於母公司業主", df.columns[i]] / df.loc["本期淨利（淨損）", df.columns[i]], 2)
    df_row = pd.DataFrame(FS, columns=df.columns, index=account_titles)
    df = pd.concat([df, df_row], axis=0)

    # 合併原始資產負債表
    account_titles = [
        "流動資產",
        "非流動資產",
        "資產總計",
        "流動負債",
        "非流動負債",
        "負債總計",
        "股本",
        "資本公積",
        "保留盈餘",
        "權益總計",
        "每股參考淨值",
    ]
    df2 = pd.DataFrame({}, index=account_titles)
    for y in range(int(year_s), int(year_e)+1):
        s_end = int(season_e) if y == int(year_e) else 4
        for s in range(1, s_end+1):
            fn = f"../data/qtr_report/bs_{str(y)}{str(s)}.csv"
            _ = pd.read_csv(fn, encoding="utf-8", header=0, index_col="公司代號")

            new_col = {}
            for item in account_titles:
                try:
                    new_col[item] = float(_.loc[int(ticker), item])
                except:
                    new_col[item] = 0
            df_col = pd.DataFrame({str(y)+str(s): new_col})
            df2 = pd.concat([df2, df_col], axis=1, sort=False)

    # 計算各項比例 (5年期)
    FS = np.zeros((4, df.shape[1]), dtype=float)
    account_titles = [
        "負債比",
        "流動比",
        "ROA",
        "ROE",
    ]
    for i in range(df.shape[1]):
        FS[0][i] = round(
            100 * df2.loc["負債總計", df2.columns[i]] / df2.loc["資產總計", df2.columns[i]], 2)
        FS[1][i] = round(
            100 * df2.loc["流動資產", df2.columns[i]] / df2.loc["流動負債", df2.columns[i]], 2)
        FS[2][i] = round(
            100 * df.loc["本期淨利（淨損）", df.columns[i]] / df2.loc["資產總計", df2.columns[i]], 2)
        FS[3][i] = round(
            100 * df.loc["本期淨利（淨損）", df.columns[i]] / df2.loc["權益總計", df2.columns[i]], 2)
    df_row = pd.DataFrame(FS, columns=df.columns, index=account_titles)
    df2 = pd.concat([df2, df_row], axis=0)
    df = pd.concat([df, df2], axis=0)
    df.to_csv(fn_dst, encoding="utf-8")

if __name__ == "__main__":
    os.system("clear")
    #=== 先分析三年期資料（始於2018），在此之前的網頁格式不同，需另行處理
    cal_fin_idx("2454", "2020", "3", 3)