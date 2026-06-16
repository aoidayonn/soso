from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View

from soso.models import AccountUser, ShoppingItem, ShoppingItemsincart
from soso.forms import UserLoginForm, UserCreateForm, UserUpdateForm, SearchForm


# ──────────────────────────────────────
# ヘルパー：ログイン中のユーザーを取得
# ──────────────────────────────────────
def get_login_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    try:
        return AccountUser.objects.get(user_id=user_id)
    except AccountUser.DoesNotExist:
        return None


# ──────────────────────────────────────
# ログイン
# ──────────────────────────────────────
class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "soso/login.html", {"form": form})

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

        request.session["user_id"] = request.POST["user_id"]
        return redirect("soso:top_page")


# ──────────────────────────────────────
# ログアウト
# ──────────────────────────────────────
class UserLogout(View):
    def get(self, request):
        request.session.flush()
        return redirect("soso:user_login")


# ──────────────────────────────────────
# 新規会員登録
# ──────────────────────────────────────
class UserCreate(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "soso/registerUser.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if not form.is_valid():
            return render(request, "soso/registerUser.html", {"form": form})

        if AccountUser.objects.filter(user_id=form.cleaned_data["user_id"]).exists():
            context = {
                "form": form,
                "error": "そのユーザ名は既に使用されています",
            }
            return render(request, "soso/registerUser.html", context)

        return render(request, "soso/registerUserConfirm.html", {"form": form})


class UserCreateConfirm(View):
    def get(self, request):
        return redirect("soso:user_create")

    def post(self, request):
        new_user = AccountUser()
        new_user.user_id = request.POST["user_id"]
        new_user.password = request.POST["password_1"]
        new_user.name = request.POST["name"]
        new_user.address = request.POST["address"]
        new_user.save()

        request.session["user_id"] = new_user.user_id
        return render(request, "soso/registerUserCommit.html", {"user_info": new_user})


# ──────────────────────────────────────
# トップページ（検索フォーム表示）
# ──────────────────────────────────────
class TopPage(View):
    def get(self, request):
        user_info = get_login_user(request)
        form = SearchForm()
        context = {
            "user_info": user_info,
            "form": form,
        }
        return render(request, "soso/main.html", context)


# ──────────────────────────────────────
# 商品検索（GET）
# ──────────────────────────────────────
class SearchResult(View):
    def get(self, request):
        form = SearchForm(request.GET)

        products = None
        if form.is_valid():
            category = form.cleaned_data.get("category", "すべて")
            keyword = form.cleaned_data.get("keyword", "")

            category_map = {"帽子": 1, "鞄": 2}
            category_id = category_map.get(category)

            products = ShoppingItem.objects.all()
            if category_id:
                products = products.filter(category_id=category_id)
            if keyword:
                products = products.filter(name__icontains=keyword)

        context = {
            "form": form,
            "products": products,
        }
        return render(request, "soso/searchResult.html", context)


# ──────────────────────────────────────
# 会員情報の確認
# ──────────────────────────────────────
class UserInfo(View):
    def get(self, request):
        user_info = get_login_user(request)
        if not user_info:
            return redirect("soso:user_login")
        return render(request, "soso/userInfo.html", {"user_info": user_info})


# ──────────────────────────────────────
# 会員情報の変更
# ──────────────────────────────────────
class UserUpdate(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        form = UserUpdateForm(initial={
            "user_id": user.user_id,
            "name": user.name,
            "address": user.address,
        })
        return render(request, "soso/updateUser.html", {"form": form})

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        form = UserUpdateForm(request.POST, initial={"user_id": user.user_id})

        if not form.is_valid():
            return render(request, "soso/updateUser.html", {"form": form})

        return render(request, "soso/updateUserConfirm.html", {"form": form})


class UserUpdateConfirm(View):
    def get(self, request):
        return redirect("soso:user_update")

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        user.password = request.POST["password_1"]
        user.name = request.POST["name"]
        user.address = request.POST["address"]
        user.save()

        return render(request, "soso/updateUserCommit.html", {"user_info": user})


# ──────────────────────────────────────
# 退会
# ──────────────────────────────────────
class UserWithdrawConfirm(View):
    def get(self, request):
        user_info = get_login_user(request)
        if not user_info:
            return redirect("soso:user_login")
        return render(request, "soso/withdrawConfirm.html", {"user_info": user_info})


class UserWithdrawCommit(View):
    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        name = user.name
        user.delete()
        request.session.flush()
        return render(request, "soso/withdrawCommit.html", {"name": name})


# ──────────────────────────────────────
# 商品詳細
# ──────────────────────────────────────
class ItemDetail(View):
    def get(self, request, item_id):
        item_info = ShoppingItem.objects.get(item_id=item_id)
        numbers = range(1, item_info.stock + 1)
        return render(request, "soso/itemDetail.html", {
            "item_info": item_info,
            "numbers": numbers,
        })


# ──────────────────────────────────────
# ショッピングカート
# ──────────────────────────────────────
class ShoppingCart(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_items = ShoppingItemsincart.objects.filter(user=user)
        total = sum(ci.item.price * ci.amount for ci in cart_items)

        context = {
            "cart_items": cart_items,
            "total": total,
        }
        return render(request, "soso/cart.html", context)

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        item_id = request.POST.get("item_id")
        num = int(request.POST.get("num", 1))

        item = ShoppingItem.objects.get(item_id=item_id)

        cart_item = ShoppingItemsincart.objects.filter(
            user=user,
            item=item,
        ).first()

        if cart_item:
            cart_item.amount += num
            cart_item.booked_date = timezone.now()
            cart_item.save()
        else:
            ShoppingItemsincart.objects.create(
                user=user,
                item=item,
                amount=num,
                booked_date=timezone.now(),
            )

        return redirect("soso:shopping_cart")