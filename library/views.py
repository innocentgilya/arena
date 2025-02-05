from django.http import HttpResponse,FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from .models import Book, UserBook, PastPapaer, UserPastPaper, GRADE_CHOICES
from userauths.models import Profile, User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from .utils import quicksort
from django.contrib import messages
import os
from BookShelf.common.decorators import subscription_required

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
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'library/index.html', context)




def home(request):
    '''show all the available textbooks & past papers'''
    books = Book.objects.all().order_by("-id")
    context = {'books': books}
    return render(request, 'library/home.html', context)




@login_required
def search(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    query = request.GET.get('q')
    books = []
    past_papers = []
    
    if query:
        # Search in both Books and Past Papers models
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(subject__icontains=query) |
            Q(grade__icontains=query)
        ).order_by('title')

        past_papers = PastPapaer.objects.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(grade__icontains=query)
        ).order_by('title')  # Adjust fields based on your PastPaper model

    context = {
        'profile': profile,
        'books': books,
        'past_papers': past_papers,
        'query': query,
    }
    return render(request, 'library/search_results.html', context)





@login_required
def autocomplete_search(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    query = request.GET.get('term', '')  # 'term' is typically used for autocomplete queries
    books = []
    past_papers = []
    results = []

    if query:
        # Search in the Book model
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        ).order_by('title')

        # Search in the PastPaper model
        past_papers = PastPapaer.objects.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query)
        ).order_by('title')

    # Add books to results
    for book in books:
        book_json = {
            'id': book.id,
            'label': f"Book: {book.title}",  # Prefix with "Book" to differentiate
            'value': book.title,
        }
        results.append(book_json)

    # Add past papers to results
    for paper in past_papers:
        paper_json = {
            'id': paper.id,
            'label': f"Past Paper: {paper.title}",  # Prefix with "Past Paper" to differentiate
            'value': paper.title,
        }
        results.append(paper_json)

    return JsonResponse(results, safe=False)



#######BOOKS########
#######BOOKS########
@login_required
def profile_home(request, profile_id):
    '''a function that displays all books available to read to a certain profile'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    grades = GRADE_CHOICES
    books = Book.objects.all().order_by("-id")
    

    context = {
        'profile': profile,
        'grades' : grades,
        'books': books,
    }
    return render(request, 'library/profile_home.html', context)



#######PAST-PAPERS########
#######PAST-PAPERS########
@login_required
def Ppapers_home(request, profile_id):
    '''a function that displays all books available to read to a certain profile'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    grades = GRADE_CHOICES
    ppapers = PastPapaer.objects.all().order_by("-id")
    

    context = {
        'profile': profile,
        'grades' : grades,
        'ppapers': ppapers,
    }
    return render(request, 'library/Ppapers.html', context)




#######BOOKS########
#######BOOKS########
@login_required
def books_by_grade(request, grade, profile_id):
    '''A function that orders books by grade books by grade '''
    
    profile = get_object_or_404(Profile,  id=profile_id, user=request.user)
    books = Book.objects.filter(grade=grade)
    grades = GRADE_CHOICES

    context = {
        'profile': profile,
        'books': books,   
        'grades': grades,     
    }
    return render(request, 'library/books_by_grade.html', context)




@login_required
def save_book(request, profile_id, book_id):
    '''Function to save books '''

    if  request.method == 'POST':

        profile = get_object_or_404(Profile, id=profile_id, user=request.user)
        book = get_object_or_404(Book, id=book_id)
        user_book, created = UserBook.objects.get_or_create(user=request.user, profile=profile, book=book)
        user_book.save()

        
        return redirect('library:profile-home',profile_id=profile.id)



@login_required
def myshelf(request, profile_id): 
    '''shows all books associated with a particular user'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    recently_read_books = UserBook.objects.filter(profile=profile, current=True).order_by('-id')
    saved_books = UserBook.objects.filter(profile=profile, read=False)


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

    def pdf_streaming():
        with open(pdf_path, 'rb') as pdf_file:
            while chunk := pdf_file.read(8192):  # Read in 8KB chunks
                yield chunk

    try:
        response = StreamingHttpResponse(pdf_streaming(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="book.pdf"'
        return response
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

    return render(request, 'library/opn-book2.html', context)


@login_required
def get_cloudpdf_config(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Generate the configuration server-side
    config = {
        "documentId": book.drive_file_id, # Securely fetch the ID
        "appBarColored": True,
        "themeColour": "#E5F0FF",
        "darkMode": True,
        "token": "",  # Add server-side token if needed
    }
    return JsonResponse(config)



# uses the google's api 
#@login_required
#def get_pdf_link(request, book_id):
    # Get the book from the database
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    # Validate user access (Optional: Add logic to check if the user has paid for this book)
    #if not user_has_access(request.user, book):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    # Generate the Google Drive link
    file_id = book.drive_file_id  
    download_url = generate_pdf_link(file_id)
    
    return JsonResponse({'url': download_url})


#def set_file_permissions(file_id):
    client_secret_file = 'BookShelf/credentials/vernal-segment-445921-k9-8c59294dc1a2.json'
    api_name = 'drive'
    api_version = 'v3'
    scopes = ['https://www.googleapis.com/auth/drive']
    
    service = create_service(client_secret_file, api_name, api_version, scopes)

    permission_body = {
        'type': 'anyone',
        'role': 'reader'
    }

    service.permissions().create(
        fileId=file_id,
        body=permission_body
    ).execute()






#@login_required
#def open_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound("Book not found.")

    file_id = book.drive_file_id
    pdf_url = generate_pdf_link(file_id)  
    return render(request, 'library/opn-book2.html', {'pdf_url': pdf_url, 'book': book})





#to serve the pdf past papaer
@login_required
def serve_pdf1(request, pastpaper_id):
    pastpaper = get_object_or_404(PastPapaer, id=pastpaper_id)
    pdf_path = pastpaper.pdf_file.path
    print(f"Serving PDF from: {pdf_path}")  # Debug log

    try:
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="pastpaper.pdf"'
            return response
    except FileNotFoundError:
        raise Http404("The requested PDF file was not found.")



@login_required
def open_pastpapaer(request, profile_id, id):
    '''the view to open the book'''
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    pastpaper = get_object_or_404(PastPapaer, id=id)
    context = {
        'pastpaper': pastpaper,
        'profile': profile,
    }

    return render(request, 'library/open-pastpaper.html', context)














