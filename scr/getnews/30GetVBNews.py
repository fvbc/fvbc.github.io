
# module
import arrow
import requests
from bs4 import BeautifulSoup


# main

OutFile = 'vbnews.html'
HtmlBody = "<html>\n<head>\n<title>Volleyball News</title>\n<link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n"

JPNow = arrow.now('Asia/Tokyo')
WeekList = ['日','月','火','水','木','金','土']
HtmlBody += '取得日時: ' + JPNow.format('YYYY/MM/DD ') + WeekList[int(JPNow.format('d'))] + JPNow.format(' HH:mm') + "<br>\n"

FeedList = ['https://news.yahoo.co.jp/rss/media/getsuv/all.xml', 'https://news.yahoo.co.jp/rss/media/vbm/all.xml']

# 各フィードを巡回する繰り返し
for FeedURL in FeedList:
  print(FeedURL)

  # RSSの取得
  # URLに接続して情報取得
  r = requests.get(FeedURL)
  
  # ソースをHTMLとして解釈して取得
  HTMLStr = r.text
  soup = BeautifulSoup(HTMLStr, 'lxml-xml')

  # アイテムの分析とHTMLの作成
  # タイトル
  HtmlBody += "<p>====================================<br>\n"
  HtmlBody += f"<a href=\"{soup.link.string}\" target=\"_blank\" rel=\"noopener noreferrer\"> 🏐 {soup.title.string}</a><br>\n"
  HtmlBody += "====================================</p>\n"

  for item in soup.findAll('item'):
#    print(f"<a href=\"{item.link.string}\">{item.title.string}</a>")
    HtmlBody += f"<p><a href=\"{item.link.string}\" target=\"_blank\" rel=\"noopener noreferrer\">{item.title.string}</a></p><br>\n"

  HtmlBody += "<br>\n"

HtmlBody += "\n</body>\n</html>\n"
print(HtmlBody)

# 文字列をHTMLファイルに書き出し
with open(OutFile, "w") as file:
    file.writelines(HtmlBody)

