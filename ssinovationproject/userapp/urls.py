from django.urls import path
from .views import *
urlpatterns = [
    path('', home_view,name="home"),
    path('login/', login_view,name="login"),
    path('delete/<uid>/', delete,name="delete"),
    path('update/<uid>/', update,name="update"),
    path('logout/', logout_view,name="logout"),
    path('signup/', signup_view,name="signup"),
    path('upload/', change_profile_picture,name="upload"),
    path('delete-picture/', delete_profile_picture,name="delete-picture"),
    path('profile-update/', profile_update,name="profile-update"),

    path('change-password/', change_password,name="change-password"),
    path('otp/', otp_view,name="otp"),

    path('detail-profile/<uid>/', details_profile,name="detail-profile"),
    path('detail-status/<uid>/', details_status,name="detail-status"),

    path('search/', search,name="search"),

    path('add-status/', add_status,name="add-status"),
] 
