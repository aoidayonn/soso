from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import View
#from message.models import Article
#from message.forms import ArticleCreateForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "soso/top.html")

    def post(self, request, *args, **kwargs):
        pass
