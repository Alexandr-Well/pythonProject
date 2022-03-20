from django.urls import path
from .views import RegisterUser, LoginUser, logout_user, ViewUserInfo, GetFile

urlpatterns = [
    path('registration/', RegisterUser.as_view(), name="registration"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path("user_info/", ViewUserInfo.as_view(), name="user_info"),
    path("get_file/", GetFile.as_view(), name="get_file"),
]