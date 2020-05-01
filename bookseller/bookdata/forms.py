from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
import bcrypt
from .models import Author, Publisher, Catagory, Catalog, Orderdetails


class Userform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Enter Your Username'}
    ), required=True, max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'placeholder': 'Enter Name'}
    ), required=True, max_length=50)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Enter Your Email'}
    ), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Enter Your Password'}
    ), required=True, max_length=50)
    Confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Confirm Password'}
    ), required=True, max_length=50)

    class Meta():
        model = User
        fields = ['username', 'first_name',
                  'email', 'password', 'Confirm_password']

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match = User.objects.get(username=user)
        except:
            if user.isdigit():
                raise forms.ValidationError("Username Can't Be Only Numeric")
            if len(user) <= 2:
                raise forms.ValidationError(
                    "Username Must Have Atleast 3 Chracter")
            return self.cleaned_data['username']
        raise forms.ValidationError('Username Already Exist')

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if name:
            if len(name) < 2:
                raise forms.ValidationError(
                    "Name Must Have Atleast 2 Character")
            elif name.isdigit():
                raise forms.ValidationError(
                    'Name Should Not Contain All Numeric Value')
            else:
                return self.cleaned_data['first_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            mat = validate_email(email)
        except:
            return forms.ValidationError("Email Is Not Correct Format")
        return email

    def clean_Confirm_password(self):
        pas = self.cleaned_data['password']
        cpas = self.cleaned_data['Confirm_password']
        min_length = 8
        if pas and cpas:
            if pas != cpas:
                raise forms.ValidationError(
                    'Password and Confirm Password Are Not Matched')
            else:
                if len(pas) < min_length:
                    raise forms.ValidationError(
                        'Password Should Have Atleast 8 Chracter')
                if pas.isdigit():
                    raise forms.ValidationError(
                        'Password Should Not contain only Numeric Give mix of Numeric and Alphabets')
                if pas.isalpha():
                    raise forms.ValidationError(
                        'Password Should Not contain only Alphabets Give mix of Numeric and Alphabets')


class Author_value(forms.ModelForm):
    authorid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter Author Id'}
    ), required=True, max_length=50)

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'myauthorname',
               'placeholder': 'Enter Author Name'}
    ), required=True, max_length=50)

    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'myauthorcity',
               'placeholder': 'Enter Author City'}
    ), required=True, max_length=50)
    country = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'myauthorcountry',
               'placeholder': 'Enter Author Country'}
    ), required=True, max_length=50)

    class Meta():
        model = Author
        fields = ['authorid', 'name', 'city', 'country']

    def clean_authorid(self):
        authorid = self.cleaned_data['authorid']
        if authorid:
            if not authorid.isdigit():
                raise forms.ValidationError(
                    'User id should contain only digits')
            elif all([v == '0' for v in authorid]):
                raise forms.ValidationError(
                    "Author id can't contains all zero")
            elif len(authorid) < 2:
                raise forms.ValidationError(
                    'User id must contain atleast two digits')
            else:
                return self.cleaned_data['authorid']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 2:
                raise forms.ValidationError(
                    'Author name must contains atleast two characters')
            elif name.isdigit():
                raise forms.ValidationError(
                    'Name must contains only sequence of chracters')
            else:
                return self.cleaned_data['name']

    def clean_city(self):
        city = self.cleaned_data['city']
        if city:
            if len(city) < 2:
                raise forms.ValidationError(
                    'City must contains atleast two characters')
            elif city.isdigit():
                raise forms.ValidationError(
                    'City must contains only sequence of chracters')
            else:
                return self.cleaned_data['city']

    def clean_country(self):
        country = self.cleaned_data['country']
        if country:
            if len(country) < 2:
                raise forms.ValidationError(
                    'Country must contains atleast two characters')
            elif not country.isalpha():
                raise forms.ValidationError(
                    'Country must contains only sequence of chracters')
            else:
                return self.cleaned_data['country']


class Publisher_Details(forms.ModelForm):
    publisherid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter Publisher Id'}
    ), required=True, max_length=50)

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'myname',
               'placeholder': 'Enter Publisher Name'}
    ), required=True, max_length=50)

    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'mycity',
               'placeholder': 'Enter Publisher City'}
    ), required=True, max_length=50)
    country = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'mycountry',
               'placeholder': 'Enter Publisher Country'}
    ), required=True, max_length=50)

    class Meta():
        model = Publisher
        fields = ['publisherid', 'name', 'city', 'country']

    def clean_publisherid(self):
        publisherid = self.cleaned_data['publisherid']
        if publisherid:
            if not publisherid.isdigit():
                raise forms.ValidationError(
                    'Publisher id should contain only digits')
            elif all([v == '0' for v in publisherid]):
                raise forms.ValidationError(
                    "Publisher id can't contains all zero")
            elif len(publisherid) < 2:
                raise forms.ValidationError(
                    'Publisher id must contain atleast two digits')
            else:
                return self.cleaned_data['publisherid']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 2:
                raise forms.ValidationError(
                    'Publisher name must contains atleast two characters')
            elif name.isdigit():
                raise forms.ValidationError(
                    'Name must contains only sequence of chracters')
            else:
                return self.cleaned_data['name']

    def clean_city(self):
        city = self.cleaned_data['city']
        if city:
            if len(city) < 2:
                raise forms.ValidationError(
                    'City must contains atleast two characters')
            elif city.isdigit():
                raise forms.ValidationError(
                    'City must contains only sequence of chracters')
            else:
                return self.cleaned_data['city']

    def clean_country(self):
        country = self.cleaned_data['country']
        if country:
            if len(country) < 2:
                raise forms.ValidationError(
                    'Country must contains atleast two characters')
            elif not country.isalpha():
                raise forms.ValidationError(
                    'Country must contains only sequence of chracters')
            else:
                return self.cleaned_data['country']


class Catagory_Details(forms.ModelForm):
    catagoryid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter Catagory Id'}
    ), required=True, max_length=50)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter Some Description'}
    ), required=True, min_length=4)

    class Meta():
        model = Catagory
        fields = ['catagoryid', 'description']

    def clean_catagoryid(self):
        catagoryid = self.cleaned_data['catagoryid']
        if catagoryid:
            if not catagoryid.isdigit():
                raise forms.ValidationError(
                    'Catagory id should contain only digits')
            elif all([v == '0' for v in catagoryid]):
                raise forms.ValidationError(
                    "Catagory id can't contains all zero")
            elif len(catagoryid) < 2:
                raise forms.ValidationError(
                    'Catagory id must contains atleast two digit')
            else:
                return self.cleaned_data['catagoryid']


class Catalog_Details(forms.ModelForm):
    bookid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter book id'}
    ), required=True, max_length=50)

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter title'}
    ), required=True, max_length=50)
    year_of_publish = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'catalogpublish',
               'placeholder': 'Enter Published Year'}
    ), required=True, max_length=5)
    authorid = forms.ModelChoiceField(queryset=Author.objects.all())
    publisherid = forms.ModelChoiceField(queryset=Publisher.objects.all())
    catagoryid = forms.ModelChoiceField(queryset=Catagory.objects.all())
    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter Price'}
    ), required=True, max_length=50)

    class Meta():
        model = Catalog
        fields = ['bookid', 'title', 'year_of_publish',
                  'price', 'authorid', 'publisherid', 'catagoryid']

    def clean_bookid(self):
        bookid = self.cleaned_data['bookid']
        if bookid:
            if not bookid.isdigit():
                raise forms.ValidationError(
                    'Book id should contain only digits')
            elif all([v == '0' for v in bookid]):
                raise forms.ValidationError(
                    "Book id can't contains all zero")
            elif len(bookid) < 2:
                raise forms.ValidationError(
                    'Book id must contain atleast two digits')
            else:
                return self.cleaned_data['bookid']

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 2:
                raise forms.ValidationError(
                    'Title must contains atleast two characters')
            else:
                return self.cleaned_data['title']

    def clean_year_of_publish(self):
        year_of_publish = self.cleaned_data['year_of_publish']
        if year_of_publish:
            if len(year_of_publish) < 4:
                raise forms.ValidationError(
                    'Year of Publish must contains atleast four digits')
            elif not year_of_publish.isdigit():
                raise forms.ValidationError(
                    'Year_of_publish must contains only digits')
            else:
                return self.cleaned_data['year_of_publish']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price:
            if not price.isdigit():
                raise forms.ValidationError(
                    'Price must contains only digits')
            else:
                return self.cleaned_data['price']


class Order_Details_Form(forms.ModelForm):
    orderno = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter order no'}
    ), required=True, max_length=50)

    quantity = forms.IntegerField(max_value=20)
    bookid = forms.ModelChoiceField(queryset=Catalog.objects.all())

    class Meta():
        model = Orderdetails
        fields = ['orderno', 'bookid', 'quantity']

    def clean_orderno(self):
        orderno = self.cleaned_data['orderno']
        if orderno:
            if not orderno.isdigit():
                raise forms.ValidationError(
                    'Book id should contain only digits')
            elif all([v == '0' for v in orderno]):
                raise forms.ValidationError(
                    "Book id can't contains all zero")
            elif len(orderno) < 2:
                raise forms.ValidationError(
                    'Book id must contain atleast two digits')
            else:
                return self.cleaned_data['orderno']

