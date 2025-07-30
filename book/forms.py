from django import forms

from .models import Author, Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','file','author','description','price','quantity','published_year','image']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name','birthday','country','phone_number']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if len(full_name) < 3:
            raise forms.ValidationError('Full name must be at least 3 characters long')
        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        import re
        pattern = r'^\+998\d{9}$'
        if not re.match(pattern,phone_number):
            raise forms.ValidationError('Phone number must be entered in the format: +998123456789')
        return phone_number






class EmailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
    from_email = forms.EmailField()
    to_email = forms.EmailField()