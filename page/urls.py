from django.urls import path

from page.views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, \
    ContactCreateView, ContactListView, ContactDetailView, ContactUpdateView, ContactDeleteView

urlpatterns = [
    path('create/',ProductCreateView.as_view(),name='create'),
    path('list/',ProductListView.as_view(),name='list'),
    path('detail/<int:pk>/',ProductDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',ProductUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',ProductDeleteView.as_view(),name='delete'),

    # contact crud url
    path('create-contact/',ContactCreateView.as_view(),name='create_contact'),
    path('list-contact/',ContactListView.as_view(),name='list-contact'),
    path('detail-contact/<str:slug>',ContactDetailView.as_view(),name='detail-contact'),
    path('update-contact/<str:slug>',ContactUpdateView.as_view(),name='update-contact'),
    path('delete-contact/<str:slug>',ContactDeleteView.as_view(),name='delete-contact'),
]

