from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, F, OuterRef, Subquery, Max, Case, When

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
    latest_msg = Talk.objects.filter(
        Q(talk_from=OuterRef("pk"), talk_to=user)
        | Q(talk_from=user, talk_to=OuterRef("pk"))
    ).order_by("-time")
    
    #OuterRef('pk')でannotateでフィールドを追加するレコードのpkを取ってきている

    friends = (
        User.objects.exclude(id=user.id)
        .annotate(
            latest_msg_talk=Subquery(latest_msg.values("contents")[:1]),
            latest_msg_time=Subquery(latest_msg.values("time")[:1]),
        )
        .order_by(F("latest_msg_time").desc(nulls_last=True))
    )
    #Subquery(latest_msg.~)でlatest_magをサブクエリとして使用している

    params = {
        'friends':friends,
        'form':form,
    }
    return render(request, 'myapp/friends.html', params)

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    talk = Talk.objects.select_related(
        "talk_from", "talk_to"
    ).filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")

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
    if request.method == 'POST':
        user = request.user
        form = FindForm(request.POST)
        find = request.POST['find']

        latest_msg = Talk.objects.filter(
        Q(talk_from=OuterRef("pk"), talk_to=user)
        | Q(talk_from=user, talk_to=OuterRef("pk"))
        ).order_by("-time")
        friends = (User.objects.filter(
            Q(username__icontains = find)|
            Q(email__icontains = find)
            )
            .annotate(
            latest_msg_talk=Subquery(latest_msg.values("contents")[:1]),
            latest_msg_time=Subquery(latest_msg.values("time")[:1]),    
        ).order_by(F("latest_msg_time").desc(nulls_last=True))
        )

        
    params = {
        'friends':friends,
        'form':form,
    }
    return render(request, 'myapp/find.html', params)


# latest_info = Talk.objects.filter(
#                 Q(talk_from=user,talk_to=friend)| Q(talk_from=friend,talk_to=user)
#             ).order_by('time').last()