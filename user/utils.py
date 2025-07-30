# from django.contrib.auth.models import Group, Permission
# # from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import PermissionDenied
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.shortcuts import redirect
#
# from book.models import Book
# from user.models import Role, CustomUser
# from book_u4.settings import EMAIL_HOST_USER as my_email
#
#
#
# def checking_user(func):
#     def wrapper(request,*args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect("login")
#         return func(request,*args, **kwargs)
#     return wrapper
#
#
# def checking_role(func):
#     def wrapper(request,*args,**kwargs):
#         if  request.user.is_authenticated:
#             if request.user.role == Role.ADMIN:
#                 return func(request,*args,**kwargs)
#             else:
#                 raise PermissionDenied
#         else:
#             raise PermissionDenied
#     return wrapper
#
#
# # content_type=ContentType.objects.get_for_model(Book)
# permission=Permission.objects.get(codename="delete_book")
# group,created=Group.objects.get_or_create(name="editor")
# user=CustomUser.objects.get(username="newadmin1")
# user.groups.add(group)
# group.permissions.add(permission)
#
#
#
#
# def send_email_u4(request):
#     send_mail(
#         subject="Bugungi kechgi ovqat",
#         message="bu bir sir ",
#         from_email= my_email,
#         recipient_list=[my_email,"abdullagulomjonov2306@gmail.com"],
#         fail_silently=False,
#     )
#     return HttpResponse("ok")
#
#
#
