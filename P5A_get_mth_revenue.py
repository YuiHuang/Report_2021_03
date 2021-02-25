import os
import requests
import pandas as pd

def get_mth_revenue(year, month):
    """彙總每月營收
    #=== year: 2018 (西元年)
    #=== month: 9 (前面不補0)
    """
    fn_dst = f"../data/mth_revenue/rev_{year}{month}.csv"
    fn_sii = f"../data/mth_revenue/_table_sii_{year}{month}.csv"
    get_mops_revenue('sii', year, month)

    fn_otc = f"../data/mth_revenue/_table_otc_{year}{month}.csv"
    get_mops_revenue('otc', year, month)

    tables = [
        pd.read_csv(fn_sii, encoding='utf-8', index_col=0),
        pd.read_csv(fn_otc, encoding='utf-8', index_col=0),
    ]

    df = pd.concat(tables, ignore_index=True)
    df.sort_values(by='公司代號', inplace=True, ascending=True)
    df = df.reset_index(drop=True)
    df.to_csv(fn_dst, encoding='utf-8')
    os.remove(fn_sii)
    os.remove(fn_otc)
# ======================================================================
def get_mops_revenue(market, year, month):
    """抓取HTML》公開資訊觀測站》彙總報表》資訊揭露》每月營收
    #=== market: sii (上市) | otc (上櫃)
    #=== year: 2018 (西元年)
    #=== month: 9 (前面不補0)
    """
    url = 'https://mops.twse.com.tw/nas/t21/'
    url += market
    url += '/t21sc03_' + str(int(year)-1911) + '_' + month + '_0.html'
    try:
        r = requests.get(url)
        r.encoding = 'big5'
    except:
        print('** Fail: 月營收 (%s)' % market)
        return

    tables = pd.read_html(r.text)
    new_tables = []
    for i, df in enumerate(tables):
        if df.shape[1] >= 3:
            df = df.iloc[0:df.shape[0]-1, 0:3]
            df.columns = ["公司代號", "公司名稱", "月營收"]
            if df.shape[0] > 0:
                new_tables.append(df)

    fn = f"../data/mth_revenue/_table_{market}_{year}{month}.csv"
    df = pd.concat(new_tables, ignore_index=True)
    df.to_csv(fn, encoding='utf-8')
    print(f"... {market} 月營收: {df.shape}")
# ======================================================================
if __name__ == '__main__':
    os.system('clear')
    year = "2015"
    month = "2"
    get_mth_revenue(year, month)