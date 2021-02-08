#===擷取上市公司的收盤價格
import requests
date = 20210205
url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&"
url += f"date={date}&type=ALLBUT0999&_=1563499391572"
r = requests.post(url)
print(r.text)

#===將從網站下載的CSV格式資料存下來
csv_filename = f"../data/price_{date}.csv"
with open(csv_filename, "w", encoding="utf-8") as f:
    f.write(r.text)

#===清理資料原始資料，方便交由後續的程式解讀
lines = r.text.split('\n')
print(lines[:5])

gobbler = {ord(" "): None}
tokens = [i.translate(gobbler) for i in lines if
          (len(i.split('",')) >= 15 or len(i.split(',')) >= 15) and i[0] != '=']
print(tokens)

#===將資料轉換成容易處理的pandas DataFrame (df)
import pandas as pd
from io import StringIO

df = pd.read_csv(StringIO("\n".join(tokens)), header=1, index_col="證券代號")
print(df.shape)

#===選取想要保留的資料
selected_cols = ["證券名稱", "收盤價", "本益比"]
df = df[selected_cols]
print(df[:5])

