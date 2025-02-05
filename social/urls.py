from django.urls import path
from social import views

app_name = 'social'
urlpatterns = [
    path('chat/<int:id>/', views.chat_view, name='chat_view'),
]
