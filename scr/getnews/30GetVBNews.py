
# module
import arrow
import requests
from bs4 import BeautifulSoup


# main

#OutFile = 'vbnews.html'
OutFile = 'vbinfo.html'

# ================================================================================================================
# HTML冒頭
# ================================================================================================================

HtmlBody = "<html>\n<head>\n<title>Volleyball News</title>\n<link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n"
HtmlBody += "<div class=\"bg_pattern Diagonal_v2\"></div>\n"

JPNow = arrow.now('Asia/Tokyo')
WeekList = ['日','月','火','水','木','金','土']
HtmlBody += '更新日時: ' + JPNow.format('YYYY/MM/DD ') + WeekList[int(JPNow.format('d'))] + JPNow.format(' HH:mm') + "<br>\n"


# ================================================================================================================
# 参考リソース
# ================================================================================================================
HtmlBody += "<p>【 バレーボール小学生ルール 】</p>\n"
HtmlBody += f"<a href=\"https://jeva-web.com/wsyst/wp-content/uploads/2023/04/2023_kyougikisoku.pdf\" target=\"_blank\" rel=\"noopener noreferrer\"> 🏐 小学生バレーボール競技規則 [日本小学生バレーボール連盟]</a><br>\n"


# ================================================================================================================
# バレーRSS
# ================================================================================================================
HtmlBody += "<p>【 注目ニュース 】</p>\n"
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
  HtmlBody += "<ul>\n"

  for item in soup.findAll('item'):
#    print(f"<a href=\"{item.link.string}\">{item.title.string}</a>")
#    HtmlBody += f"<p><a href=\"{item.link.string}\" target=\"_blank\" rel=\"noopener noreferrer\">{item.title.string}</a></p><br>\n"
    HtmlBody += f"  <li><a href=\"{item.link.string}\" target=\"_blank\" rel=\"noopener noreferrer\">\n  {item.title.string}</a></li>\n"
    DescriStr = item.description.string.replace('\n','').replace('\u3000','')
    HtmlBody += f"  <p>　{DescriStr}...</p>\n"
  HtmlBody += "</ul>"
  HtmlBody += "<br>\n"


# ================================================================================================================
# HTML末尾
# ================================================================================================================
HtmlBody += "\n</body>\n</html>\n"
# print(HtmlBody)


# ================================================================================================================
# HTML書き出し
# ================================================================================================================
with open(OutFile, "w") as file:
    file.writelines(HtmlBody)

