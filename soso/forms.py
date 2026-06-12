from django import forms

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password = forms.CharField(label="パスワード:", max_length=256)


class UserCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password_1 = forms.CharField(label="パスワード:", max_length=256)
    password_2= forms.CharField(label="パスワード(確認):", max_length=256)
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        
class UserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password_1 = forms.CharField(label="パスワード:", max_length=256)
    password_2= forms.CharField(label="パスワード(確認):", max_length=256)
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")

