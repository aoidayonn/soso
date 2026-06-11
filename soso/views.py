from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from soso.models import AccountUser
from soso.forms import UserLoginForm, UserCreateForm

class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        context = {
            "form":form,
        }
        return render(request, "soso/login.html", context)
    def post(self, request):
        pass


class UserCreate(View):
    def get(self, request):
        form = UserCreateForm()
        context = {
            "form":form,
        }
        return render(request, "soso/registerUser.html", context)
    
    def post(self, request):
        form = UserCreateForm(request.POST)
        if not form.is_valid():
            context = {
                "form":form
            }
            return render(request, "soso/registerUser.html", context)
        
        user_exists = AccountUser.objects.filter(
            name=form.cleaned_data["user_id"]
        ).exists()

        if user_exists:
            context = {
                "form": form,
                "error": "ユーザ名またはメールアドレスは既に使用されています",
            }
            return render(request, "soso/registerUser.html", context)

        context = {
            "form":form,
            }
        return render(request, "soso/registerUserConfirm.html", context)
    

class UserCreateConfirm(View):
    def get(self, request):
        pass
    
    def post(self, request):
        new_user = AccountUser()
        new_user.user_id = request.POST["user_id"]
        new_user.password = request.POST["password_1"]
        new_user.name = request.POST["name"]
        new_user.address = request.POST["address"]
        new_user.save()

        context = {
            "name":new_user.name
        }

        return render(request, "soso/registerUserCommit.html", context)