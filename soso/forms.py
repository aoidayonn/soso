from django import forms


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,
    )


class UserCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password_1 = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,
    )
    password_2 = forms.CharField(
        label="パスワード(確認):",
        max_length=256,
        widget=forms.PasswordInput,
    )
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data


class UserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128, disabled=True)
    password_1 = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,   # ★ 入力時 ●●●● で隠れる
    )
    password_2 = forms.CharField(
        label="パスワード(確認):",
        max_length=256,
        widget=forms.PasswordInput,   # ★ 入力時 ●●●● で隠れる
    )
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data
    
    
class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    CATEGORY_CHOICES = [
        ("すべて", "すべて"),
        ("帽子", "帽子"),
        ("鞄", "鞄"),
    ]

    category = forms.ChoiceField(
        label="カテゴリ:",
        choices=CATEGORY_CHOICES,
        required=False,
    )
    keyword = forms.CharField(
        label="キーワード:",
        max_length=128,
        required=False,
    )