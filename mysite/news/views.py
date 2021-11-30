from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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

    return render(request, "news/news_search.html", {},)
