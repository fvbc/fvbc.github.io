# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 情報取得スクリプト
# 
# 予定：
# 配当推移取得
# 主要インデックス表示
# 
# 個別詳細：
#  - 信用倍率
#  - 時価総額
#  - 大口動向
#  - 次回決算
#  - 次回権利確定日、支払い日
# 関連ニュース
# 業種に関する情報表示
# 業種別統計：ヒートマップ、騰落率、
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# モジュールのインポート
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from IPython.display import HTML, display
from datetime import datetime
import datetime
import arrow
import sys
import os
import time
import japanize_matplotlib  
import requests
from bs4 import BeautifulSoup
import re

print("処理開始")

# 出力ファイルの指定
OutFileName = "k/index.html"
#OutFileName = "/workspaces/fvbc.github.io/k/index.html"


HtmlBody = "<html>\n<head>\n<title>GetInfoooooo!</title>\n</head>\n<body>\n"

#DtNow = datetime.datetime.now()
JPNow = arrow.now('Asia/Tokyo')
WeekList = ['日','月','火','水','木','金','土']

# print( '今の時間: ' + DtNow.strftime('%Y/%m/%d %H:%M') )
# print( '今の時間: ' + JPNow.format('YYYY/MM/DD ') + WeekList[int(JPNow.format('d'))] + JPNow.format(' HH:mm') )


#HtmlBody += '処理日時: ' + DtNow.strftime ( '%Y/%m/%d %H:%M' ) + "\n"

HtmlBody += '処理日時: ' + JPNow.format('YYYY/MM/DD ') + WeekList[int(JPNow.format('d'))] + JPNow.format(' HH:mm') + "\n"



HtmlBody += "<p>※配当利回りの数字は不正確の模様。確認中。</p>\n"
HtmlBody += "<p>※日経平均、主要ETF、その他指数のチャートはいずれ対応予定。</p>\n"
HtmlBody += "<p>　Nasdaq100、SP500、DOW、日経先物、TOPIX、ドル円など</p>\n\n"


print(HtmlBody)


# 対象銘柄のリスト
symbols = ['1518.T', '1605.T', '1419.T', '1719.T']
#symbols = ['1301.T', '1414.T', '1419.T', '1420.T', '1518.T', '1605.T', '1663.T', '1719.T', '1766.T', '1801.T', '1802.T', '1820.T', '1911.T', '1925.T', '1928.T', '1934.T', '1938.T', '1941.T', '1944.T', '1951.T', '1952.T', '2053.T', '2114.T', '2229.T', '2269.T', '2270.T', '2331.T', '2337.T', '2353.T', '2393.T', '2461.T', '2503.T', '2531.T', '2540.T', '2670.T', '2676.T', '2871.T', '3002.T', '3003.T', '3105.T', '3106.T', '3109.T', '3167.T', '3183.T', '3244.T', '3289.T', '3291.T', '3407.T', '3465.T', '3489.T', '3738.T', '3941.T', '4008.T', '4008.T', '4021.T', '4041.T', '4042.T', '4042.T', '4044.T', '4063.T', '4118.T', '4151.T', '4182.T', '4189.T', '4204.T', '4208.T', '4272.T', '4410.T', '4452.T', '4452.T', '4502.T', '4503.T', '4507.T', '4540.T', '4551.T', '4665.T', '4968.T', '5020.T', '5021.T', '5101.T', '5122.T', '5185.T', '5192.T', '5201.T', '5208.T', '5332.T', '5334.T', '5706.T', '5938.T', '5947.T', '5985.T', '6089.T', '6257.T', '6268.T', '6278.T', '6284.T', '6384.T', '6454.T', '6486.T', '6625.T', '7164.T', '7272.T', '7278.T', '7433.T', '7480.T', '7840.T', '8001.T', '8058.T', '8173.T', '8306.T', '8309.T', '8316.T', '8341.T', '8354.T', '8411.T', '8418.T', '8425.T', '8473.T', '8566.T', '8584.T', '8593.T', '8630.T', '8725.T', '8725.T', '8917.T', '8934.T', '8999.T', '8999.T', '9432.T', '9433.T', '9434.T', '9513.T', '9513.T', '9733.T', '9795.T', '9852.T', '9869.T', '9880.T', '9882.T', '9997.T']
#symbols = ['1301.T', '1414.T', '1419.T', '1420.T', '1518.T', '1605.T', '1663.T', '1719.T', '1766.T', '1801.T', '1802.T', '1820.T', '1911.T', '1925.T', '1928.T', '1934.T', '1938.T', '1941.T', '1944.T', '1951.T', '1952.T', '2053.T', '2114.T', '2229.T', '2269.T', '2270.T', '2331.T', '2337.T', '2353.T', '2393.T', '2461.T', '2503.T', '2531.T', '2540.T', '2670.T', '2676.T', '2871.T', '3002.T', '3003.T', '3105.T', '3106.T', '3109.T', '3167.T', '3183.T', '3244.T', '3289.T', '3291.T', '3407.T', '3465.T', '3489.T', '3738.T', '3941.T', '4008.T', '4021.T', '4041.T', '4042.T', '4044.T', '4063.T', '4118.T', '4151.T', '4182.T', '4189.T', '4204.T', '4208.T', '4272.T', '4410.T', '4452.T', '4502.T', '4503.T', '4507.T', '4540.T', '4551.T', '4665.T', '4968.T', '5020.T', '5021.T', '5101.T', '5122.T', '5185.T', '5192.T', '5201.T', '5208.T', '5332.T', '5334.T', '5706.T', '5938.T', '5947.T', '5985.T', '6089.T', '6257.T', '6268.T', '6278.T', '6284.T', '6384.T', '6454.T', '6486.T', '6625.T', '7164.T', '7272.T', '7278.T', '7433.T', '7480.T', '7840.T', '8001.T', '8058.T', '8173.T', '8306.T', '8309.T', '8316.T', '8341.T', '8354.T', '8411.T', '8418.T', '8425.T', '8473.T', '8566.T', '8584.T', '8593.T', '8630.T', '8725.T', '8917.T', '8934.T', '8999.T', '9432.T', '9433.T', '9434.T', '9513.T', '9733.T', '9795.T', '9852.T', '9869.T', '9880.T', '9882.T', '9997.T']


# 銘柄情報を格納するリスト
company_info = []

# 直近半年のデータを格納するディクショナリ
ohlc_data = {}

cs  = mpf.make_mpf_style(base_mpf_style='yahoo', rc={"font.family":'IPAexGothic'})


# 取得先URL生成のためのテンプレURL
BaseYhURL = "https://finance.yahoo.co.jp/quote/"

print("<info> 繰り返し処理開始。")
for symbol in symbols:
  print(f"<info> コード：{symbol}")
  
  # 変数の初期化
  YhURL=None
  r = None
  HTMLStr = None
  soup = None
  YhTitleStr = None
  StockName = None
  IdsArea = None
  IdsStr = None
  
  
  # ------------------------------------------------
  # 日本語情報を取得する処理
  YhURL=BaseYhURL+symbol
  
  # 負荷軽減のための待機
  time.sleep(1)
  
  # URLに接続して情報取得
  r = requests.get(YhURL)
  
  # ソースをHTMLとして解釈して取得
  HTMLStr = r.text
  soup = BeautifulSoup(HTMLStr, 'html.parser')
  
  # タイトルから企業名称を取得する
  YhTitleStr = soup.title.string
  m = None
  m = re.findall('(.+?)【\d+',YhTitleStr)
  
  # 文字列を取得できなかった場合の別の対処
  if len(m) == 0:
    print("<info> タイトル取得時に通常とは異なるパターンを検知：1")
    m = re.findall('(.+?)：.*',YhTitleStr)
  
  StockName = m[0]
  
  # 業種
  IdsArea = soup.find(id="industry")
  m = None
  if IdsArea == None:
    IdsStr = "-"
  else:
    m = re.findall('^\d+(.*)$',IdsArea.text)
    IdsStr = m[0]
  
  print(f"<info> 企業名称Jp：{StockName} [{IdsStr}]")
  
  # ------------------------------------------------
  
  
  company = yf.Ticker(symbol)
  info = company.info
  
  
  company_code = symbol.split('.')[0]  # コード
  company_name = info.get('longName', 'N/A')   # 社名の取得
  sector = info.get('sector', 'N/A')  # セクター、業種
  
  ex_dividend_date = info.get('exDividendDate', 'N/A')  # 次回の権利確定日
  print(f"{ex_dividend_date}")
  
  ex_dividend_date_format = datetime.datetime.fromtimestamp(ex_dividend_date)
  ex_dividend_date_str = ex_dividend_date_format.strftime('%Y/%m/%d')
  
  previous_close = info.get('regularMarketPreviousClose', 'N/A')  # 前日終値
  dividend_yield = info.get('dividendYield', 'N/A')  # 配当利回り
  company_info.append([company_code, company_name, sector, ex_dividend_date, previous_close, dividend_yield])
  
  
  # 各銘柄の情報をHTMLファイルへ書き込み。
  HtmlBody += f"<br><br>────────────────────────────────────────"
#  HtmlBody += f"<p>{company_code}：{company_name} （{sector}）</p>\n"
  HtmlBody += f"<p>{company_code}：{StockName} （{IdsStr}）</p>\n"
  HtmlBody += f"<p>利回：{dividend_yield:.2%}  権確：{ex_dividend_date_str}  前日終値：{previous_close} 円</p>\n"
#  HtmlBody += f"<p>前日終値：{previous_close}</p>\n"
  HtmlBody += f"<img src='img/{company_code}.T_candlestick_chart.png'>\n"
  
  
  # 直近半年の4本値および売買高データを取得
  end_date = datetime.date.today()
  start_date = end_date - datetime.timedelta(days=180)  # 直近半年
  data = yf.download(symbol, start=start_date, end=end_date)
  ohlc_data[symbol] = data
  
  print("<info>追加部分：チャート作成処理")
  
  
  # ローソク足チャートの画像を作成して保存・表示
#  for symbol, data in ohlc_data.items():
  print(f"\n【デバッグエリア】変数「StockName」→{StockName}")
  time.sleep(1)
  mpf.plot(data, type="candle",title=f'{symbol} {StockName}日足6ヶ月Chart',ylabel="株価", ylabel_lower="出来高", volume=True,
#           savefig=f'/workspaces/fvbc.github.io/k/img/{symbol}_candlestick_chart.png', style=cs)
           savefig=f'k/img/{symbol}_candlestick_chart.png', style=cs)
           
#  chart_image = f'/workspaces/fvbc.github.io/k/img/{symbol}_candlestick_chart.png'
  chart_image = f'k/img/{symbol}_candlestick_chart.png'

  display(HTML(f'<img src="{chart_image}">'))
  
  print('ローソク足チャート画像が生成され、表示されました。')
  
  # 負荷軽減のための待機
  time.sleep(1)

# 繰り返しここまで



# HTMLの末尾部分を追加
HtmlBody += "\n\n</html>\n"

# 文字列をHTMLファイルに書き出し
with open(OutFileName, "w") as file:
    file.writelines(HtmlBody)


#print("出力ファイルの中身を確認↓")
#!cat index.html


# 銘柄情報を一覧で表示
df_info = pd.DataFrame(company_info, columns=['コード', '銘柄名', '業種名', '次回権利付き確定日', '前日終値', '予想配当利回り'])
display(HTML(df_info.to_html(escape=False, index=False)))

# 生成した銘柄情報をCSVファイルとして保存
#info_file = '/workspaces/fvbc.github.io/k/company_info.csv'
info_file = 'k/company_info.csv'



df_info.to_csv(info_file, index=False, encoding='utf-8')
print(f'銘柄情報が {info_file} に保存されました.')

#cs  = mpf.make_mpf_style(rc={"font.family":'IPAexGothic'})
#cs  = mpf.make_mpf_style(base_mpf_style='yahoo', rc={"font.family":'IPAexGothic'})

# ローソク足チャートの画像を作成して保存・表示
#for symbol, data in ohlc_data.items():
#    mpf.plot(data, type='candle', style='yahoo', title=f'{symbol} 価格Candlestick Chart (Last 6 Months)',
#    mpf.plot(data, type="candle",title=f'{symbol} 価格Candlestick Chart (Last 6 Months)',ylabel="株価", ylabel_lower="出来高", volume=True,
#             savefig=f'k/img/{symbol}_candlestick_chart.png', ylabel_lower='Volume', style=cs)
#             savefig=f'k/img/{symbol}_candlestick_chart.png', style=cs)
#             savefig=f'k/img/{symbol}_candlestick_chart.png')
#    chart_image = f'k/img/{symbol}_candlestick_chart.png'
#    display(HTML(f'<img src="{chart_image}">'))

#print('ローソク足チャート画像が生成され、表示されました。')

print("終わり")
