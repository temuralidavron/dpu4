from django.urls import path
# from book import views
from book.views import get_book, book_detail, create_book, edit_book, delete_book
from book import views

# from .views import *

urlpatterns=[
    path('',get_book,name='book-list'),
    path('create/',create_book,name='book-create'),
    path('detail/<int:pk>/',book_detail,name='book-detail'),
    path('edit/<int:pk>/',edit_book,name='book-edit'),
    path('delete/<int:pk>/',delete_book,name='book-delete'),

    # author crud
    path('author/',views.get_author,name='author-list'),
    path('author/create/', views.create_author, name='author-create'),
    path('detail/author/<int:pk>/', views.get_detail, name='author-detail'),
    path('edit/author/<int:pk>/', views.author_edit, name='author-edit'),


    # email
    path('email/', views.email_chat, name='email-chat'),
    path('emails/', views.send_html_email, name='email-m'),

    # to_excel
    path('excel/',views.export_to_xlsx,name='excel'),



]
