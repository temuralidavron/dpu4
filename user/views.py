from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from book.views import send_html_email
from book_u4 import settings
from user.forms import UserForm, LoginForm, ForgetPasswordForm, ChangePasswordForm, ProfileUpdateForm
from user.models import CustomUser, Code, Profile
from book_u4.settings import  EMAIL_HOST_USER as from_email

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'user/register.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=CustomUser.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('book-list')
                return HttpResponse('Form is not valid', status=400)

            return HttpResponse('Form is not valid', status=400)
    else:
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('login')


def forget_view(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = CustomUser.objects.filter(username=username).first()
            if user is not None:
                code=Code.objects.create(user=user)
                send_html_email(
                    subject="parolni tiklash",
                    from_email=from_email,
                    to_email=user.email,
                    text_content="Parolni tiklash",
                    code=code.code,
                    username=user.username,
                )
                return render(request, 'user/done.html', {'form': form})


    form = ForgetPasswordForm()
    return render(request, 'user/forget.html', {'form': form})



# def change_password_view(request):
#     username=request.GET.get('name')
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST)
#         if form.is_valid():
#             user = CustomUser.objects.filter(username=username).first()
#             code=form.cleaned_data['code']
#             password=form.cleaned_data['password']
#             re_password=form.cleaned_data['password']
#             if user is not None:
#                 user_code=Code.objects.filter(user=user,expire_date__gt=timezone.now()).first()
#                 if user_code.code != code:
#                     return HttpResponse('Form is not valid code', status=400)
#                 if password != re_password:
#                     return HttpResponse('Form is not valid password', status=400)
#
#                 return redirect('login')
#     form=ChangePasswordForm()
#     return render(request, 'user/change_password.html', {'form': form})
def change_password_view(request):
    username = request.GET.get('name')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.filter(username=username).first()
            password=form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            code = form.cleaned_data['code']
            if user is not None:
                print(timezone.now())
                user_code=Code.objects.filter(user=user,expire_date__gt=timezone.now()).first()
                if user_code.code!=code:
                    return HttpResponse('Invalid code')
                if password != re_password:
                    return HttpResponse('Invalid password')
                user.set_password(password)
                user.save()
                return redirect('login')
    form=ChangePasswordForm()
    return render(request,'user/change_password.html',{'form':form})


# GOOGLE LOGIN

def google_login(request):
    auth_url = (

        f"{settings.GOOGLE_AUTH_URL}"

        f"?client_id={settings.GOOGLE_CLIENT_ID}"

        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"

        f"&response_type=code"

        f"&scope=openid email profile"

    )

    return redirect(auth_url)

import requests
from django.http import HttpResponse
from django.conf import settings

def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Kod yo‘q", status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    # Access token olish
    token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return HttpResponse("Access token olinmadi", status=400)

    # User ma’lumotlarini olish
    user_info_response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user_info = user_info_response.json()
    # print(user_info)  # <-- bu yerda foydalanuvchi haqida ma’lumot chiqadi (email, name va hokazo)
    user,_=CustomUser.objects.get_or_create(
        username=user_info.get("given_name"),
        email=user_info.get("email"),
    )
    if user:
        login(request, user)
        return redirect('book-list')

    return redirect('login')


# Profile view

def profile_view(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    context={
        'profile':profile,
    }
    return render(request, 'user/profile.html', context)



def update_profile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    if request.method == 'POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form=ProfileUpdateForm(instance=profile)

    return render(request, 'user/update_profile.html', {'form': form})
