from django.shortcuts import redirect, render, get_object_or_404


from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, UserNameForm, TalkForm,MailChangeForm, IconChangeForm, FindForm
from django.contrib.auth import authenticate, get_user_model, login, logout

from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import Talk
from django.db.models import Q
import operator
from django.contrib.auth.decorators import login_required

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")
        else:            
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)



class Login(LoginView):
    form_class = LoginForm
    template_name = "myapp/login.html"
    

@login_required
def friends(request):
    form = FindForm()
    user = request.user
    friends = User.objects.exclude(id=user.id)
    
    info = []
    info_have = []
    info_none = []

    for friend in friends :
        latest_info = Talk.objects.filter(
                Q(talk_from=user,talk_to=friend)| Q(talk_from=friend,talk_to=user)
            ).order_by('time').last()
        if latest_info:
            info_have.append([
                friend,
                latest_info.contents,
                latest_info.time
            ])
        else:
            info_none.append([
                friend,None,None
            ])
    info_have=sorted(info_have,key=operator.itemgetter(2),reverse=True)

    info.extend(info_have)
    info.extend(info_none)

    params = {
        'info':info,
        'form':form,
    }
    return render(request, 'myapp/friends.html', params)

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    talk = Talk.objects.filter(
        Q(talk_from=user,talk_to=friend) |Q(talk_from=friend,talk_to=user)
    ).order_by('time')

    form = TalkForm()

    contexts = {
        'form':form,
        'talk':talk,
        'friend':friend,
    }

    if request.method == 'POST':
        new_talk = Talk(talk_from=user,talk_to=friend)
        form=TalkForm(request.POST,instance=new_talk)

        if form.is_valid():
            form.save()
            return redirect('talk_room',user_id)
        else:
            print(form.errors)

    return render(request, "myapp/talk_room.html", contexts)

@login_required
def setting(request):
    
    user = request.user
    param = {
        'user':user,
    }
    return render(request, "myapp/setting.html", param)

@login_required
def change_name(request, user_id):

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserNameForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            context = {
                'form':form,
                'user':user
            }
            return redirect('username_change_done')
    else:
        form=UserNameForm(instance=user)

        context={
            'form':form,
            'user':user
        }

        return render(request, 'myapp/username_change.html', context)

@login_required
def username_change_done(request):
    return render(request, 'myapp/username_change_done.html')
      
@login_required
def mail_change(request,user_id):
    user = User.objects.get(id=user_id)

    if request.method =='POST':
        form = MailChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('mail_change_done')
        
    else:
        form = MailChangeForm(instance=user)

        param = {
            'form':form,
            'user':user,
        }
        return render(request, 'myapp/mail_change.html', param)

@login_required
def mail_change_done(request):
    return render(request, 'myapp/mail_change_done.html')

@login_required
def icon_change(request, user_id):

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = IconChangeForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('icon_change_done')
        
    else:
        form = IconChangeForm(instance=user)
        param={
            'form':form,
            'user':user,
        }
        return render(request, 'myapp/icon_change.html', param)
    
@login_required    
def icon_change_done(request):
    return render(request, 'myapp/icon_change_done.html')    

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

class Password_change(PasswordChangeView):
    template_name = "myapp/password_change.html"
    success_url = reverse_lazy('setting')

def find(request):
    # if request.method == 'POST':
    #     form = FindForm(request.POST)
    #     find = request.POST['find']
    #     data = User.objects.filter(username__contains=find)

    # contexts = {
    #     'form':form,
    #     'data':data,
    # }
    # return render(request, 'myapp/find.html', contexts)

    if request.method == 'POST':
        user = request.user
        form = FindForm(request.POST)
        find = request.POST['find']
        friends = User.objects.filter(username__icontains = find)

        info = []
        info_have = []
        info_none = []

        for friend in friends :
            latest_info = Talk.objects.filter(
                Q(talk_from=user,talk_to=friend)| Q(talk_from=friend,talk_to=user)
            ).order_by('time').last()
        if latest_info:
            info_have.append([
                friend,
                latest_info.contents,
                latest_info.time
            ])
        else:
            info_none.append([
                friend,None,None
            ])
    info_have=sorted(info_have,key=operator.itemgetter(2),reverse=True)

    info.extend(info_have)
    info.extend(info_none)

    params = {
        'info':info,
        'form':form,
    }
    return render(request, 'myapp/find.html', params)