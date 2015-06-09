from django.http import Http404
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
    login as login_view,
    logout as logout_view,
    password_reset as password_reset_view,
    password_reset_done as password_reset_done_view,
    password_reset_confirm as password_reset_confirm_view,
    password_reset_complete as password_reset_complete_view
)

from users.models import User
from users.forms import UserSignupForm, UserLoginForm
from users.utils import default_token_generator


def user_signup(request):
    if request.method == 'POST':
        f = UserSignupForm(request.POST)
        if f.is_valid():
            user = f.save()

            user = authenticate(email=f.cleaned_data['email'],
                password=f.cleaned_data['password'])
            login(request, user)

            user.send_verification_mail(request)

            return redirect('home')
    else:
        f = UserSignupForm()

    return render(request, 'users/user_signup.html', {
        'form': f
    })


def user_login(request):
    return login_view(
        request,
        authentication_form=UserLoginForm,
        template_name='users/user_login.html'
    )


def user_logout(request):
    return logout_view(request, next_page='home')


@login_required
def user_verification(request):
    if request.method == 'POST':
        request.user.send_verification_mail(request)

    return render(request, 'users/user_verification.html')


def user_verify(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist):
        raise Http404

    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()

        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        raise Http404


def user_password_reset(request):
    return password_reset_view(
        request,
        template_name='users/user_password_reset.html',
        email_template_name='users/user_password_reset_email.html',
        subject_template_name='users/user_password_reset_subject.txt',
        post_reset_redirect='users:password_reset_done'
    )


def user_password_reset_done(request):
    return password_reset_done_view(
        request,
        template_name='users/user_password_reset_done.html',
    )


def user_password_reset_confirm(request, uidb64, token):
    return password_reset_confirm_view(
        request,
        token=token,
        uidb64=uidb64,
        template_name='users/user_password_reset_confirm.html',
        post_reset_redirect='users:password_reset_complete'
    )


def user_password_reset_complete(request):
    return password_reset_complete_view(
        request,
        template_name='users/user_password_reset_complete.html'
    )
