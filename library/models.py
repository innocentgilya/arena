from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from userauths.models import Profile

# Create your models here.
# Define grade choices
GRADE_CHOICES = [
    ('Grade 1', 'Grade 1'),
    ('Grade 2', 'Grade 2'),
    ('Grade 3', 'Grade 3'),
    ('Grade 4', 'Grade 4'),
    ('Grade 5', 'Grade 5'),
    ('Grade 6', 'Grade 6'),
    ('Grade 7', 'Grade 7'),
    ('Grade 8', 'Grade 8'),
    ('Grade 9', 'Grade 9'),
    ('Grade 10', 'Grade 10'),
    ('Grade 11', 'Grade 11'),
    ('Grade 12', 'Grade 12'),
]
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100,)
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES)
    subject = models.CharField(max_length=15)
    book_cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    published_date = models.DateField()
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    pdf_file = models.FileField(upload_to='book_pdfs/')

    
    def __str__(self):
        return self.title
    
    def get_pdf_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return None

    @classmethod
    def add_book(cls, title, author, published_date, grade, subject ,book_cover):
    #Create a new book instance
        new_book = cls(
            title=title, author=author, published_date=published_date, 
            grade=grade, subject=subject, book_cover=book_cover 
        )
        # Save the new book instance to the database
        new_book.save()
        return new_book

    def delete_book(self):
        '''delete the book instance from the database'''
        self.delete()


class UserBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_book', default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

# models for the past papers 
class PastPapaer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    #author = models.CharField(max_length=100)
    grade = models.CharField(max_length=15,choices=GRADE_CHOICES)
    subject = models.CharField(max_length=15)
    book_cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    published_date = models.DateField()
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    pdf_file = models.FileField(upload_to='book_pdfs/')

    
    def __str__(self):
        return self.title
    
    def get_pdf_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return None

    @classmethod
    def add_pastpaper(cls, title, published_date, grade, subject ,book_cover):
    #Create a new book instance
        new_book = cls(
            title=title, published_date=published_date, 
            grade=grade, subject=subject, book_cover=book_cover 
        )
        # Save the new Pastpapaer instance to the database
        new_book.save()
        return new_book

    def delete_book(self):
        '''delete the book instance from the database'''
        self.delete()


class UserPastPaper(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_past_papers', default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    PastPapaer = models.ForeignKey(Book, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'