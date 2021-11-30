from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewsSearchForm
from .utils import naverapi_utils as naver_api


@login_required(login_url="common:login")
def index(request):
    """
    뉴스 검색 화면으로 리다이렉트한다.
    """
    return redirect("news:news_search")


@login_required(login_url="common:login")
def news_search(request):
    """
    뉴스 검색 화면을 반환한다.
    """

    news_list = None

    if request.method == "GET":
        if len(request.GET):
            form = NewsSearchForm(request.GET)

            if form.is_valid():
                keyword = form.cleaned_data["keyword"]
                news_list = naver_api.get_news_by_hour(keyword)
        # 뉴스를 검색하지 않고 검색 페이지를 오픈할 경우에는
        # 비어 있는 폼을 반환한다.
        else:
            form = NewsSearchForm()
    else:
        form = NewsSearchForm()

    return render(
        request, "news/news_search.html", {"form": form, "news_list": news_list},
    )
