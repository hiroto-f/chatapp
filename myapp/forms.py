from django.contrib.auth.forms import UserCreationForm


class IndexForm(UserCreationForm):
    class Meta:
        fields = ['username','email','icon']