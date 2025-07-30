from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from page.forms import ProductForm
from page.models import Product, Contact


class ProductCreateView(View):
    def get(self,request):
        form = ProductForm()
        return render(request,'page/product_form.html',{'form':form})

    def post(self,request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
        return render(request,'page/product_form.html',{'form':form})


class ProductListView(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request,'page/product_list.html',{'products':products})



class ProductDetailView(View):
    def get(self,request,pk=None):
        products = get_object_or_404(Product, pk=pk)
        return render(request,'page/product_detail.html',{'product':products})



class ProductUpdateView(View):
    def get(self,request,pk=None):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request,'page/product_form.html',{'form':form})

    def post(self,request,pk=None):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('list')
        return render(request,'page/product_form.html',{'form':form})



class ProductDeleteView(View):
    def get(self,request,pk=None):
        product = get_object_or_404(Product, pk=pk)
        return render(request,'page/product_delete.html',{'product':product})

    def post(self,request,pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('list')



# generic crud
class ContactListView(ListView):
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'  # object_list
    # paginate_by = 10
    # page_obj = get_object_or_404(Contact, pk=1)


    def get_queryset(self):
        return Contact.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        m=Book.objects.all()
        context['books']=m
        return context

class ContactCreateView(CreateView):
    model = Contact
    fields = ['name','email','message']
    template_name = 'contact/contact_form.html'
    success_url = reverse_lazy('list-contact')


class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contact/contact_detail.html'
    context_object_name = 'contact'

    def get_object(self):
        return Contact.objects.get(pk=self.kwargs['pk'])


class ContactUpdateView(UpdateView):
    model = Contact
    fields = ['name','email','message']
    success_url = reverse_lazy('list-contact')
    template_name = 'contact/contact_form.html'


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contact/contact_delete.html'
    success_url = reverse_lazy('list-contact')
    context_object_name = 'contact'


