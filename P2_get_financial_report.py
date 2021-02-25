import os
import requests
import pandas as pd

def get_mops_csv(typek, report_id, year, season):
    """抓取HTML》公開資訊觀測站》彙總報表》財務報表》
    #=== typek: sii (上市) | otc (上櫃)
    #=== report_id: 綜合損益表 (Income Statement), 資產負債表 (Balance Sheet)
    #=== year: 目標財報的年度
    #=== season: 目標財報的季度
    """
    if report_id == "is":
        url = "https://mops.twse.com.tw/mops/web/ajax_t163sb04"
    elif report_id == "bs":
        url = "https://mops.twse.com.tw/mops/web/ajax_t163sb05"
    else:
        print("** Fail: report_id error")
        return

    values = {
            "step": 1,
            "firstin": "true",
            "off": 1,
            "TYPEK": typek,
            "year": str(int(year) - 1911),
            "season": "0" + season,
    }

    try:
        r = requests.post(url, values)
        r.encoding = "utf-8"
        print(f"** Pass: 財務報表 ({typek}, {report_id}): {url}")
    except:
        print(f"** Fail: 財務報表 ({typek}, {report_id}): {url}")
        return

    fn_init = f"../data/qtr_report/raw_data/_{typek}_{report_id}_{year}{season}_"
    tables = pd.read_html(r.text)
    for i, df in enumerate(tables):
        fn = fn_init + str(i) + ".csv"
        print(f"get_mops_csv: table #{i}")
        df.to_csv(fn, encoding="utf-8")
# ======================================================================
def get_qtr_report(report_id="is", year="2020", season="3"):
    """
    #=== report_id: 綜合損益表 (Income Statement), 資產負債表 (Balance Sheet)
    #(註) 上市公司(sii)的網站頁面有7 (#0~6)張表格，一般行業是在第四張表(#3)
    #(註) 上櫃公司(otc)的網站頁面有4 (#0~3)張表格，一般行業是在第三張表(#2)
    #=== year: 目標財報的年度
    #=== season: 目標財報的季度
    """
    get_mops_csv("sii", report_id, year, season)
    get_mops_csv("otc", report_id, year, season)

    fn_dst = f"../data/qtr_report/{report_id}_{year}{season}.csv"
    fn_sii = f"../data/qtr_report/raw_data/_sii_{report_id}_{year}{season}_3.csv"
    fn_otc = f"../data/qtr_report/raw_data/_otc_{report_id}_{year}{season}_2.csv"

    tables = [
        pd.read_csv(fn_sii, encoding="utf-8", index_col=0, header=0),
        pd.read_csv(fn_otc, encoding="utf-8", index_col=0, header=0),
    ]
    print(f"... combining DataFrames: {tables[0].shape}, {tables[1].shape}")
    df = pd.concat(tables, ignore_index=True)
    df = df.sort_values(by="公司代號", ascending=True)
    df = df.reset_index(drop=True)
    df.to_csv(fn_dst, encoding="utf-8")
# ======================================================================
if __name__ == "__main__":
    os.system("clear")
    """
    years = ["2016", "2017"]
    season_e = 4
    for i in range(len(years)):
        if i == len(years) - 1:
            seasons = season_e
        else:
            seasons = 4

        for j in range(1, seasons+1):
            get_qtr_report("is", years[i], str(j))
            get_qtr_report("bs", years[i], str(j))
    """