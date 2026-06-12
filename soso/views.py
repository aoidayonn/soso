from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from soso.models import AccountUser
from soso.forms import UserLoginForm, UserCreateForm, UserUpdateForm

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
                "error": "そのユーザ名は既に使用されています",
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

        request.session['user_id'] = new_user.user_id

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


class UserLogout(View):
    def get(self, request):
        request.session.flush()
        return redirect('soso:user_login')


class UserInfo(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        user_info = AccountUser.objects.get(user_id=user_id)

        return render(request, "soso/userInfo.html", {
            'user_info': user_info
        })
    def post(self, request):
        pass


class UserUpdate(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        user = AccountUser.objects.get(user_id=user_id)

        #formに初期値
        form = UserUpdateForm(initial={
            'user_id': user.user_id,
            'name': user.name,
            'address': user.address,
        })

        context = {
            "form":form,
        }
        return render(request, "soso/updateUser.html", context)
    def post(self, request):
        form = UserUpdateForm(request.POST)
        if not form.is_valid():
            context = {
                "form":form
            }
            return render(request, "soso/updateUser.html", context)
        
        user_id = request.session.get('user_id')

        user_exists = AccountUser.objects.filter(
            user_id=request.POST["user_id"],
        ).exclude(user_id=user_id).exists()

        if user_exists:
            context = {
                "form": form,
                "error": "そのユーザ名は既に使用されています",
            }
            return render(request, "soso/updateUser.html", context)

        context = {
            "form":form,
            }
        return render(request, "soso/updateUserConfirm.html", context)


class UserUpdateConfirm(View):
    def get(self, request):
        pass
    

    def post(self, request):
        user_id = request.session.get('user_id')
        user = AccountUser.objects.get(user_id=user_id)

        user.user_id = request.POST["user_id"]
        user.password = request.POST["password_1"]
        user.name = request.POST["name"]
        user.address = request.POST["address"]
        user.save()

        request.session['user_id'] = user.user_id

        form = UserUpdateForm(request.POST)
        context = {
            "form":form
        }

        return render(request, "soso/updateUserCommit.html", context)
    

class UserWithdrawConfirm(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.get(user_id=user_id)
        context = {
            'user_info':user_info
        }

        return render(request, "soso/withdrawConfirm.html", context)
    def post(self, request):
        pass


class UserWithdrawCommit(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        request.session.flush()
        user = AccountUser.objects.get(user_id=user_id)
        user_name = user.name
        user.delete()
        context = {
            'name':user.name
        }

        return render(request, "soso/withdrawCommit.html", context)
    def post(self, request):
        pass
