from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic import View
from soso.models import AccountUser, ShoppingItem, ShoppingItemsincart
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
            user_id=form.cleaned_data["user_id"]
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
        context = {
            'user_info': user_info
        }
        return render(request, "soso/main.html", context)

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
        user_id = request.session.get('user_id')
        form = UserUpdateForm(request.POST, initial={'user_id': user_id})
        if not form.is_valid():
            context = {
                "form":form,
                "user_id": user_id,
            }
            return render(request, "soso/updateUser.html", context)

        context = {
            "form":form,
            "user_id": user_id,
            }
        return render(request, "soso/updateUserConfirm.html", context)


class UserUpdateConfirm(View):
    def get(self, request):
        pass
    

    def post(self, request):
        user_id = request.session.get('user_id')
        user = AccountUser.objects.get(user_id=user_id)

        user.password = request.POST["password_1"]
        user.name = request.POST["name"]
        user.address = request.POST["address"]
        user.save()

        form = UserUpdateForm(request.POST, initial={'user_id': user_id})
        context = {
            "form":form,
            'user_id':user_id,
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
        pass
    def post(self, request):
        user_id = request.session.get('user_id')       
        user = AccountUser.objects.get(user_id=user_id)
        user.delete()
        request.session.flush()

        context = {
            'name':user.name
        }
        return render(request, "soso/withdrawCommit.html", context)


class SearchResult(View):
    def get(self, request):
        pass
    def post(self, request):
        category = request.POST['category']
        keyword = request.POST['keyword']

        if category == "すべて":
            category_id=False
        elif category =="帽子":
            category_id=1
        else:
            category_id=2

        products = ShoppingItem.objects.all()
        if category_id:
            products = products.filter(category_id=category_id)
        if keyword:
            products = products.filter(name__icontains=keyword)

        context = {
            'category':category,
            'keyword':keyword,
            'products':products,

        }
        return render(request, "soso/searchResult.html", context)


class itemDetail(View):
    def get(self, request, item_id):
        item_info = ShoppingItem.objects.get(item_id=item_id)
        numbers = range(1, item_info.stock + 1)
        context = {
            'item_info':item_info,
            'numbers':numbers,
        }
        return render(request, "soso/itemDetail.html", context)
    def post(self, request):
        pass


class ShoppingCart(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        cart_items = ShoppingItemsincart.objects.filter(user_id=user_id)
        context = {
            'cart_items':cart_items,
        }
        return render(request, "soso/cart.html", context)
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('soso:user_login')

        item_id = request.POST.get('item_id')
        num = int(request.POST.get('num'))

        cart_item = ShoppingItemsincart.objects.filter(
        user_id=user_id,
        item_id=item_id
        ).first()

        if cart_item:
            cart_item.amount += num
            cart_item.booked_date = timezone.now()
            cart_item.save()
        else:
            ShoppingItemsincart.objects.create(
                user_id=user_id,
                item_id=item_id,
                amount=num,
                booked_date=timezone.now()
            )

        cart_items = ShoppingItemsincart.objects.filter(user_id=user_id)

        context = {
            'cart_items':cart_items,
        }
        return render(request, "soso/cart.html", context)
