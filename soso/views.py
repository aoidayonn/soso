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
        form = UserLoginForm(request.POST)

        user_exists = AccountUser.objects.filter(
            user_id=request.POST["user_id"],
            password=request.POST["password"],
        ).exists()

        if not user_exists:
            context = {
                "form": form,
                "error": "ユーザ名またはパスワードが違います",
            }
            return render(request, "soso/login.html", context)
        else:
            user_info = AccountUser.objects.get(user_id=request.POST["user_id"])
            request.session['user_id'] = user_info.user_id
            return redirect('soso:top_page')


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
    

class TopPage(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        user_info = None
        if user_id:
            user_info = AccountUser.objects.get(user_id=user_id)

        return render(request, "soso/main.html", {
            'user_info': user_info
        })

    def post(self, request):
        pass



class UserInfo(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        user_info = AccountUser.objects.get(user_id=user_id)

        return render(request, "soso/userInfo.html", {
            'user_info': user_info
        })
    def post(self, request):
        pass
