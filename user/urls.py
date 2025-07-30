from django.urls import path

# from user.utils import send_email_u4
from user.views import register, login_view, logout_view, forget_view, change_password_view, google_login, \
    google_callback, profile_view, update_profile

urlpatterns = [
    path('',register,name='register'),
    path('google/login/',google_login,name='google_login'),
    path('google/login/callback/',google_callback,name='google_login'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    # path('send/',send_email_u4,name='send'),
    path('forget/',forget_view,name='forget'),
    path('change/',change_password_view,name='change'),
    path('profile/',profile_view,name='profile'),
    path('profile/update/',update_profile,name='profile-update'),
]