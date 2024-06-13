import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

def scrape_news_articles():
    # 네이버 뉴스에서 긴급재난문자를 검색합니다.
    query = "긴급재난문자"
    url = f"https://search.naver.com/search.naver?query={query}&where=news"

    # requests를 사용하여 HTML을 가져옵니다.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 검색 결과에서 뉴스 기사들을 선택합니다.
    news_articles = soup.select('.news_area')

    articles = []
    for i in range(3):
        article_info = {}
        article = news_articles[i]
        # 기사 제목과 기자 이름을 가져옵니다.
        article_info['news_title'] = article.select_one('.news_tit').text.strip()
        article_info['reporter_name'] = article.select_one('.info_group .info').text.strip()
        articles.append(article_info)

    return articles

@app.route("/")
def news_scrape():
    news = scrape_news_articles()
    first_article = news[0]
    second_article = news[1]
    third_article = news[2]
    return render_template('5projct.html', first_article=first_article, second_article=second_article, third_article=third_article)

if __name__ == "__main__":
    app.run(debug=True, port=8080)