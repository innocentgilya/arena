'''Defines the urls for the library application'''

from django.urls import path
from library import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'library'
urlpatterns = [
    #The url that welcomes you to the Study arena website
    path('', views.index, name='index'),
    #The url that takes you to the Homepage
    path('home/', views.home, name='home'),
    #The url that takes you to the personal page
    path('myshelf/<int:user_id>/<int:profile_id>/', views.myshelf, name='myshelf'),
    #the url that takes you to ...
    #path('add_book/<int:book_id>/', views.add_book, name='add_book'),
    # The url to open the book pdf file
    path('book/<int:profile_id>/<int:id>/', views.open_book, name='open-book'),

    
    # to save a book
    path('save-book/<int:book_id>/', views.save_book, name='save-book'),
    # url to a hompage associated specificaly to aparticular user
    path('profile/<int:profile_id>/home/', views.profile_home, name='profile-home'),
    # url to search 
    path('profile/<int:user_id>/<int:profile_id>/search/', views.search, name='search'),
    #url to to serve the PDF files securely
    path('serve-pdf/<int:book_id>/', views.serve_pdf, name='serve_pdf'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)