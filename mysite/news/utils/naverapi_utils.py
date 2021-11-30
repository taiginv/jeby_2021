import json, re
import urllib.request
import urllib.parse
from dateutil.parser import parse
from datetime import timedelta
from django.conf import settings
from django.utils import timezone


def call(keyword, display=10, start=1, sort="date"):
    """
    네이버 검색 API를 호출한다.
    """

    values = {
        "query": keyword,
        "display": display,
        "start": start,
        "sort": sort,
    }

    params = urllib.parse.urlencode(values, quote_via=urllib.parse.quote)
    url = "https://openapi.naver.com/v1/search/news.json?" + params

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", settings.NAVER_API_ID)
    request.add_header("X-Naver-Client-Secret", settings.NAVER_API_SECRET)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result = json.loads(response_body.decode("utf-8")).get("items")
    else:
        print(rescode)
        result = None

    return result


def get_news(keyword, start_time=None, end_time=None):
    """
    주어진 키워드 사용하여 모든 결과를 조회한다.
    start_time과 end_time이 지정될 경우 구간 내 결과를 반환한다.
    """

    start = 1
    display = 100

    result = []
    flag = True
    while flag:
        news_list = call(keyword, display, start, "date")
        if news_list:
            for news in news_list:
                # end_time이 존재하고 end_time보다 pubDate가 이후일 경우
                # 다음 news 처리로 넘어 간다.
                if end_time and end_time < parse(news["pubDate"], ignoretz=True):
                    continue

                # start_time이 존재하고 start_time보다 뉴스 발행시간이 이전일 경우
                # result 리스트 생성을 중지한다.
                if start_time and start_time > parse(news["pubDate"], ignoretz=True):
                    flag = False
                    break

                # 개별 뉴스에 키워드를 입력한다.
                news["keyword"] = keyword

                # 개별 뉴스의 발행시간을 datetime 형식으로 변환하여 다시 입력한다.
                news["pubDate"] = parse(news["pubDate"], ignoretz=True)

                # 개별 뉴스에서 언론사 URI 추출을 위한 정규식 패턴을 생성한다.
                p = re.compile(r"^https?://([\w.-]*).*")
                if news.get("originallink"):
                    m = p.search(news.get("originallink"))
                # originallink가 없을 경우 link 값을 사용한다.
                else:
                    m = p.search(news.get("link"))
                    news["originallink"] = news.get("link")

                # 개별 뉴스에 언론사 정보를 입력한다.
                if m is not None:
                    uri = m.group(1)
                    news["siteuri"] = uri
                else:
                    print("URI 추출 실패")
                    print(f'originallink : {news.get("originallink")}')
                    print(f'link : {news.get("link")}')

                result.append(news)

            # 검색한 뉴스 개수가 display 개수와 동일할 경우
            # start에 100을 더한 후 다시 뉴스를 검색한다.
            if len(news_list) == display:
                start += 100
                if start > 1000:
                    break
            else:
                break
        else:
            flag = False

    return result


def get_news_by_hour(keyword, start_hour=12, end_hour=0):
    """
    start_hour와 end_hour 구간 내 뉴스 리스트를 반환한다.
    """

    now = timezone.now()
    end_time = now + timedelta(hours=-end_hour)
    start_time = end_time + timedelta(hours=-start_hour)

    result = get_news(keyword, start_time, end_time)

    return result
