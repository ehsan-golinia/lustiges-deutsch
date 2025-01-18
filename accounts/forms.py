from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'username',
        'class': 'form-control form-control-lg',
    }),
        required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'name': 'password',
        'class': 'form-control form-control-lg',
    }),
        required=True)


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'first_name',
        'class': 'form-control form-control-lg',
        }),
        required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'last_name',
        'class': 'form-control form-control-lg',
        }),
        required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'username',
        'class': 'form-control form-control-lg',
        }),
        required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'name': 'password',
        'class': 'form-control form-control-lg',
        }),
        required=True)
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'name': 'password2',
        'class': 'form-control form-control-lg',
    }),
        required=True)


class UpdateForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'first_name',
        'class': 'form-control form-control-lg',
        }),
        required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'last_name',
        'class': 'form-control form-control-lg',
        }),
        required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'email',
        'name': 'email',
        'class': 'form-control form-control-lg',
    }),
        required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'username',
        'class': 'form-control form-control-lg',
        }),
        required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'name': 'password',
        'class': 'form-control form-control-lg',
        }),
        required=False)
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'name': 'password2',
        'class': 'form-control form-control-lg',
    }),
        required=False)
