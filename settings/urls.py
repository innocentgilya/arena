from django.urls import path
from settings import views
from settings.views import ProfileUpdate


app_name = 'settings'

urlpatterns = [
    path('profile/<int:profile_id>/update/', ProfileUpdate.as_view(), name='profile_update'),

    path('profile/<int:profile_id>/delete/', views.profile_delete, name='profile_delete'),


    # url for landing you to the account settings page
    #path('profile/<int:profile_id>/account_settings/', views.account_display, name='account_display')
    path('account/<int:user_id>/<int:profile_id>/', views.account_display, name='account_display'),


    path('account/<int:user_id>/', views.account_settings_display, name='account_settings_display'),


    path('delete-account/', views.account_delete, name='account_delete'),
]
