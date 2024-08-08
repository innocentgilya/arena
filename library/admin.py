from django.contrib import admin
from .models import Book, UserBook

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'grade', 'subject', 'book_cover', 'pdf_file']

#class UserBook(admin.ModelAdmin):
    #list_display = ['user', 'profile', 'book', 'current', 'read', '']


admin.site.register(Book, UserAdmin)
admin.site.register(UserBook)


