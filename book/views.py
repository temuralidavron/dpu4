import openpyxl
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# from user.utils import checking_user, checking_role
from .models import Book, Author
from .forms import AuthorForm, BookForm, EmailForm


# @permission_required('book.view_book', raise_exception=True)
def get_book(request):
    q=request.GET.get('q')
    books=Book.objects.all()
    if q:
        books=books.filter(Q(title__icontains=q)|Q(description__icontains =q))
    else:
        books=books
    paginator = Paginator(books, 2)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context={
        'books':page_obj,
        'page_obj':page_obj,
    }
    return render(request,'book/book_list.html',context)

# @checking_user
def book_detail(request,pk):
    book=Book.objects.filter(pk=pk).first()
    context={
        'book':book
    }
    return render(request,'book/book_detail.html',context)
# @checking_role
# @checking_user
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            desc=form.save(commit=False)
            desc_suz=form.cleaned_data['description']
            desc.description=f"{desc_suz} salomlar bu qoshildi"
            desc.save()

            return redirect('book-list')
    else:
        form = BookForm()

    context = {
        'form': form
    }
    return render(request, 'book/book_form.html', context)




# def create_book(request):
    # title = request.POST.get('title')
    # print(title)
    # if request.method=='POST':
    #     title=request.POST.get('title')
    #     description=request.POST.get('description')
    #     price=request.POST.get('price')
    #     published_year=request.POST.get('published_year')
    #     Book.objects.create(
    #         title=title,
    #         description=description,
    #         price=price,
    #         published_year=published_year
    #     )
    #     return redirect('book-list')

    # return render(request,'book/create_book.html')
# @checking_role
# @permission_required('book.change_book', raise_exception=True)
def edit_book(request,pk):
    book=Book.objects.filter(pk=pk).first()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm(instance=book)

    return render(request, 'book/book_form.html', {'form': form})


# def edit_book(request,pk):
#     book=Book.objects.get(pk=pk)
#     if request.method=='POST':
#         title=request.POST.get('title',book.title)
#         description=request.POST.get('description',book.description)
#         price=request.POST.get('price',book.price)
#         published_year=request.POST.get('published_year',book.published_year)
#         if title and description and price and published_year:
#             book.title=title
#             book.description=description
#             book.price=price
#             book.published_year=published_year
#             book.save()
#             return redirect('book-list')


    # return render(request,'book/create_book.html',{'book':book})



def delete_book(request,pk):
    book=Book.objects.get(pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book-list')
    return render(request,'book/book_delete.html',{'book':book})


# auth crud

def create_author(request):
    if request.method=='POST':
        form=AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
        else:
            return render(request,'author/create_author.html',{'form':form})
    elif request.method=='GET':
        form=AuthorForm()
    else:
        form=AuthorForm()

    return render(request,'author/create_author.html',{'form':form})



def get_author(request):
    authors=Author.objects.all()
    context={
        'authors':authors
    }
    return render(request,'author/author_list.html',context)

def get_detail(request,pk):
    author=Author.objects.get(pk=pk)
    context={
        'author':author
    }
    return render(request,'author/author_detail.html',context)


def author_edit(request,pk):
    author=Author.objects.get(pk=pk)
    if request.method=='POST':
        form=AuthorForm(request.POST,instance=author)
        if form.is_valid():
            form.save()
            return redirect('author-list')
        else:
            return render(request,'author/create_author.html',{'form':form})
    else:
        form=AuthorForm(instance=author)
        return render(request,'author/create_author.html',{'form':form})



def email_chat(request):
    if request.method=='POST':
        form=EmailForm(request.POST)
        if form.is_valid():
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
            from_email=form.cleaned_data['from_email']
            to_email=form.cleaned_data['to_email']
            send_mail(
                subject,
                message,
                from_email,
                recipient_list=[to_email]
            )
            return redirect('book-list')
    form=EmailForm()
    return render(request,'book/email_chat.html',{'form':form})


from django.core.mail import EmailMultiAlternatives


def send_html_email(subject,from_email,to_email,text_content,code,username):
    subject =subject

    from_email = from_email
    to = [to_email]

    text_content="parol almashtirish"
    html_content = f"""
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kodni tasdiqlash</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <tr>
            <td style="padding: 20px; text-align: center; background-color: #34495e; color: white; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                <h2>Kodni tasdiqlash</h2>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px; text-align: center;">
                <p>Hurmatli foydalanuvchi,</p>
                <p>Quyidagi 6 xonali kod orqali ro‘yxatdan o‘tishni yoki parolni tiklashni yakunlashingiz mumkin:{code}</p>
                <p style="font-size: 32px; font-weight: bold; letter-spacing: 8px; margin: 20px 0;"></p>
                <p>Yoki quyidagi tugmani bosib jarayonni davom ettiring:</p>
                <a href="http://127.0.0.1:8000/user/change/?name={username}" style="background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Kodni tasdiqlash</a>
                <p style="margin-top: 30px;">Agar siz bu so‘rovni yubormagan bo‘lsangiz, iltimos, bu xabarni e’tiborsiz qoldiring.</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px; text-align: center; font-size: 12px; color: #888;">
                © 2025 Sayt nomi. Barcha huquqlar himoyalangan.
            </td>
        </tr>
    </table>
</body>
</html>
"""
    email = EmailMultiAlternatives(subject, text_content,
                                   from_email, to)

    email.attach_alternative(html_content, "text/html")

    email.send()
    return redirect('book-list')




def export_to_xlsx(request):
    workbook=openpyxl.Workbook()
    sheet = workbook.active
    sheet.title="Kitob"
    sheet.append([
        'id',
        'title',
        'description',
        'price',
        'quantity',

    ])
    books=Book.objects.all()
    for book in books:
        sheet.append([
            book.id,
            book.title,
            book.description,
            book.price,
            book.quantity,
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=u4.xlsx'
    workbook.save(response)
    return response
