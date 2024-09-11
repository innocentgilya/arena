from django.http import HttpResponse,FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserBook
from userauths.models import Profile, User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os

# Create your views here.

def index(request):
    """The index page for StudyArena"""
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        # Redirect to the profile list view if authenticated
        return redirect('userauths:profile_list')
    else:
        profile = None

    context = {
        'profile': profile,
    }
    return render(request, 'library/index.html', context)

def home(request):
    '''show all the available textbooks & past papers'''
    books = Book.objects.all().order_by("-id")
    context = {'books': books}
    return render(request, 'library/home.html', context)

@login_required
def search(request, profile_id, user_id):
    user_id = request.user.id
    profile = get_object_or_404(Profile, user_id=user_id, id=profile_id, user=request.user)    
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(subject__icontains=query) |
            Q(grade__icontains=query)
        )

    context = {
        'profile': profile,
        'books': books,
        'query': query,
    }
    return render(request, 'library/search_results.html', context)

@login_required
def profile_home(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    books = Book.objects.all().order_by("-id")
    

    context = {
        'profile': profile,
        'books': books,
    }
    return render(request, 'library/profile_home.html', context)

@login_required
def save_book(request, book_id):
    '''Function to save books '''
    if not request.user.is_authenticated:
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)
    user_book.current = True
    user_book.save()

    return redirect('home', profile_id=request.user.profiles.first().id)

@login_required
def myshelf(request, profile_id, user_id): 
    '''shows all books associated with a particular user'''
    #user_books = UserBook.objects.filter(user=request.user)
    #context = {'user_books': user_books}
    #return render(request, 'library/library.html', context)
    user_id = request.user.id
    profile = get_object_or_404(Profile, user_id=user_id, id=profile_id, user=request.user)
    recently_read_books = UserBook.objects.filter(user=request.user, profile=profile, current=True).order_by('-id')
    saved_books = UserBook.objects.filter(user=request.user, profile=profile, read=False)


    context = {
        'profile': profile,
        'recently_read_books': recently_read_books,
        'saved_books': saved_books,
    }
    return render(request, 'library/myshelf.html', context)



#def add_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user_book = UserBook.objects.create(user=request.user, book=book)
    return redirect('library')

#def my_books(request): # IMPORTANT change the name to save_book 
    # Retrieve recent read and saved books for the logged-in user
    recent_read_books = UserBook.objects.filter(user=request.user, read=True).order_by('-timestamp')[:5]
    saved_books = UserBook.objects.filter(user=request.user, saved=True)
    context = {{'recent_read_books': recent_read_books, 'saved_books': saved_books}}

    return render(request, 'library/my_books.html', context)

#def subjects_list(request):
    '''show all subjects for the textbooks'''
    #subject = Book.objects.filter()

@login_required
def serve_pdf(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    pdf_path = book.pdf_file.path
    print(f"Serving PDF from: {pdf_path}")  # Debug log

    try:
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("The requested PDF file was not found.")

@login_required
def open_book(request, profile_id, id):
    '''the view to open the book'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    book = get_object_or_404(Book, id=id)
    context = {
        'book': book,
        'profile': profile,
        }

    return render(request, 'library/open-book.html', context)















