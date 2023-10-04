from .models import Talk
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "icon","password1","password2")

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ["contents",]

class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username',]

class MailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email',]     

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['icon',]    
        
class FindForm(forms.Form):
    find = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'ユーザ名を入力'}))
