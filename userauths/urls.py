from django.urls import path
from userauths import views
from .views import ProfileList, ProfileCreate  

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path('profile/', views.profile, name='profile'),
      # The url to the list of profiles
    path('userauths/profilelist/', ProfileList.as_view(), name='profile_list'),
      # The url to the profile create form
    path('profile/create/', ProfileCreate.as_view(), name='profile-create'),
]