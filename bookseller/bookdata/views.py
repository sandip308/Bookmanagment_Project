from django.shortcuts import render, redirect
from .forms import Userform
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django import forms
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import Author_value, Publisher_Details, Catagory_Details, Catalog_Details, Order_Details_Form
from .models import Publisher, Author, Catalog, Orderdetails, Catagory


def homepage(request):
    return render(request, 'index.html')


# Create your views here.


def register(request):
    if request.session.has_key('is_logged'):
        return redirect('success')
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User.objects.create_user(username=username, first_name=first_name,
                                     email=email, password=password)
            messages.success(
                request, "You Have Created Your Account Successfully")
            return redirect('home')
    else:
        form = Userform()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.session.has_key('is_logged'):
        return redirect('success')
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['is_logged'] = True
                request.session['username'] = username
                return redirect('success')
            else:
                messages.error(request, "Username Or Password is Invalid")

        except ObjectDoesNotExist:
            print("Invalid User")
    return render(request, 'registration/login.html')


@login_required
def logout(request):
    try:
        auth.logout(request)
        del request.session['is_logged']
        del request.session['username']
    except:
        pass
    return redirect('home')


# Work with databases
@login_required
def success(request):
    if request.session.has_key('is_logged'):
        return render(request, 'Success.html')
    return redirect('login')


@login_required
def choice(request):
    if request.user.is_authenticated:
        return render(request, 'choice.html')


@login_required
def author(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Author_value(request.POST)
            if form.is_valid():
                author_id = form.cleaned_data['authorid']
                name = form.cleaned_data['name']
                city = form.cleaned_data['city']
                country = form.cleaned_data['country']
                form.save(commit=True)
                form = Author_value()
        else:
            form = Author_value()
        return render(request, 'author.html', {'form': form})


def Author_autocomplete(request):
    if request.is_ajax():
        queryset = Author.objects.filter(
            country__startswith=request.GET.get('search', None))
        queryset2 = Author.objects.filter(
            name__startswith=request.GET.get('search', None))
        queryset3 = Author.objects.filter(
            city__startswith=request.GET.get('search', None))
        li = []
        name = []
        city = []
        for p in queryset3:
            city.append(p.city)
        for j in queryset2:
            name.append(j.name)
        for i in queryset:
            li.append(i.country)
        data = {'list': li, 'name': name, 'city': city}
        return JsonResponse(data)


@login_required
def publisher(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Publisher_Details(request.POST)
            if form.is_valid():
                publisherid = form.cleaned_data['publisherid']
                name = form.cleaned_data['name']
                city = form.cleaned_data['city']
                country = form.cleaned_data['country']
                form.save(commit=True)
                form = Publisher_Details()
        else:
            form = Publisher_Details()
        return render(request, 'publisher.html', {'form': form})


def publisher_autocomplete(request):
    if request.is_ajax():
        queryset = Publisher.objects.filter(
            country__startswith=request.GET.get('search', None))
        queryset2 = Publisher.objects.filter(
            name__startswith=request.GET.get('search', None))
        queryset3 = Publisher.objects.filter(
            city__startswith=request.GET.get('search', None))
        li = []
        name = []
        city = []
        for p in queryset3:
            city.append(p.city)
        for j in queryset2:
            name.append(j.name)
        for i in queryset:
            li.append(i.country)
        data = {'list': li, 'name': name, 'city': city}
        return JsonResponse(data)


@login_required
def catalog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Catalog_Details(request.POST)
            if form.is_valid():
                form.save()

                form = Catalog_Details()
        else:
            form = Catalog_Details()
        return render(request, 'catalog.html', {'form': form})


def catalog_autocomplete(request):
    if request.is_ajax():
        queryset = Catalog.objects.filter(
            year_of_publish__startswith=request.GET.get('search', None))
        li = []
        for p in queryset:
            li.append(p.year_of_publish)
        data = {'list': li}
        return JsonResponse(data)


@login_required
def catagory(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Catagory_Details(request.POST)
            if form.is_valid():
                catagory_id = form.cleaned_data['catagoryid']
                description = form.cleaned_data['description']
                form.save(commit=True)
                form = Catagory_Details()
        else:
            form = Catagory_Details()
        return render(request, 'category.html', {'form': form})


@login_required
def order_details(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Order_Details_Form(request.POST)
            if form.is_valid():
                form.save()

                form = Order_Details_Form()
        else:
            form = Order_Details_Form()
        return render(request, 'orderdetails.html', {'form': form})


@login_required
def update_price(request):
    if request.user.is_authenticated:
        publisher_name = request.POST.get('publisher_name', None)
        change_price = request.POST.get('change_price', None)
        single_book = request.POST.get('book', None)
        all_publisher = Publisher.objects.all()
        all_catalog = Catalog.objects.all()
        di = {}
        ca = {}
        for i in all_publisher:
            di1 = {i.publisherid: i.name}
            di.update(di1)
        for q in all_catalog:
            ca1 = {q.title: q.price}
            ca.update(ca1)
        # select single book
        if publisher_name and change_price and single_book and request.method == 'POST':
            try:
                single_publisher = Publisher.objects.get(name=publisher_name)
                p = single_publisher.publisherid
                si_cata = Catalog.objects.filter(
                    publisherid=p, title=single_book)
                if si_cata.exists():
                    actual_price = ((int(change_price) + 100)/100)
                    for i in si_cata:
                        i.price = (i.price * actual_price)
                        i.save()
                else:
                    messages.warning(
                        request, 'The title that you have entered is wrong')
            except:
                messages.warning(
                    request, 'Publisher is invalid that you have entered')
        # select all book
        else:
            if publisher_name and change_price and request.method == 'POST':
                try:
                    publisher_book = Publisher.objects.get(name=publisher_name)
                    x = publisher_book.publisherid
                    cata = Catalog.objects.filter(publisherid=x)
                    if cata.exists():
                        actual_price = ((int(change_price) + 100)/100)
                        for i in cata:
                            i.price = (i.price * actual_price)
                            i.save()
                    elif cata.count() == 0 and publisher_name and change_price and request.method == 'POST':
                        messages.warning(
                            request, "This is new publisher,Price hasn't been updated till now")
                except:
                    messages.warning(
                        request, 'Publisher is invalid that you have entered')
        return render(request, 'updateprice.html', {'name': di, 'price': ca})


def updateprice_autocomplete(request):
    if request.is_ajax():
        queryset = Publisher.objects.filter(
            name__startswith=request.GET.get('search', None))
        queryset2 = Catalog.objects.filter(
            title__startswith=request.GET.get('search', None))
        li = []
        li1 = []
        for p in queryset:
            li.append(p.name)
        for s in queryset2:
            li1.append(s.title)
        data = {'list': li, 'title': li1}
        return JsonResponse(data)


@login_required
def author_details(request):
    if request.user.is_authenticated:
        min_no_of_books = request.POST.get('mininput', None)
        min_price = request.POST.get('minprice', None)
        year_publication = request.POST.get('minpublication', None)
        min_no_of_books2 = request.POST.get('secondminbook', None)
        min_price2 = request.POST.get('secondminprice', None)
        year_publication2 = request.POST.get('secondminyear', None)
        catalog_books = Catalog.objects.count()
        grate = False
        all_object = None
        msg = None
        if min_no_of_books2 and min_price2 and request.method == 'POST':
            p = None
            li = Catalog.objects.values_list('price', flat=True)
            if li:
                mini = min(li)
                p = Catalog.objects.filter(
                    price__range=(mini, min_price2))
                if p.exists():
                    if int(min_no_of_books2) <= p.count():
                        c = int(min_no_of_books2)
                        all_object = p.all()[:c]
                    elif int(min_no_of_books2) > p.count():
                        all_object = p.all()
                        grate = True
                elif (not p.exists()) and min_price2 and min_no_of_books2 and request.method == 'POST':
                    msg = "NO RESULT FOUND"
            else:
                msg = "NO BOOKS ARE AVAILABLE IN THIS TIME"

        elif min_no_of_books2 and year_publication2 and request.method == 'POST':
            yr = None
            yr = Catalog.objects.filter(
                year_of_publish__exact=year_publication2)
            if yr.exists():
                if int(min_no_of_books2) <= yr.count():
                    c = int(min_no_of_books2)
                    all_object = yr.all()[:c]
                elif int(min_no_of_books2) > catalog_books:
                    all_object = yr.all()
                    grate = True

            elif (not yr.exists()) and year_publication2 and min_no_of_books2 and request.method == 'POST':
                msg = "NO RESULT FOUND"
        elif min_price2 and year_publication2 and request.method == 'POST':
            yr = None
            yr = Catalog.objects.filter(
                year_of_publish__exact=year_publication2)
            if yr.exists():
                li = yr.values_list('price', flat=True)
                if li:
                    mini = min(li)
                    all_object = yr.filter(
                        price__range=(mini, min_price2))
                    if (not all_object.exists()) and min_price2 and year_publication2 and request.method == 'POST':
                        msg = "NO RESULT FOUND"
                else:
                    msg = "NO BOOKS ARE AVAILABLE IN THIS TIME"

            elif (not yr.exists()) and year_publication2 and min_price2 and request.method == 'POST':
                msg = "NO RESULT FOUND"

        else:
            if min_no_of_books and request.method == 'POST':
                if int(min_no_of_books) <= catalog_books:
                    c = int(min_no_of_books)
                    all_object = Catalog.objects.all()[:c]
                elif int(min_no_of_books) > catalog_books:
                    all_object = Catalog.objects.all()
                    grate = True
            elif min_price and request.method == 'POST':
                li = Catalog.objects.values_list('price', flat=True)
                if li:
                    mini = min(li)
                    all_object = Catalog.objects.filter(
                        price__range=(mini, min_price))
                    if (not all_object.exists()) and min_price and request.method == 'POST':
                        msg = "NO RESULT FOUND"
                else:
                    msg = "NO BOOKS ARE AVAILABLE IN THIS TIME"
            elif year_publication and request.method == 'POST':
                all_object = Catalog.objects.filter(
                    year_of_publish__exact=year_publication)
                if (not all_object.exists()) and year_publication and request.method == 'POST':
                    msg = "NO RESULT FOUND"

        return render(request, 'authordetails.html', {'filter1_id': all_object, 'grate': grate, 'total': catalog_books, 'msg': msg})


@login_required
def author_maxsales(request):
    if request.user.is_authenticated:
        arr = Orderdetails.objects.values_list('quantity', flat=True)
        if arr:
            maxi = max(arr)
            order = Orderdetails.objects.filter(quantity=maxi)
            x = set()
            di = dict()
            for i in order:
                x.add(i.bookid.authorid.name)
            p = list(x)
            res = {'sandip': p}
        else:
            res = {'sandip': False}
        return render(request, 'maxsales.html', res)


@login_required
def update_delete(request):
    if request.user.is_authenticated:
        return render(request, 'updatedelete.html')


@login_required
def delete_author(request):
    if request.user.is_authenticated:
        all_obj = Author.objects.all()
        if request.method == 'POST':
            all_object = request.POST.getlist('allcheck[]')
            for i in all_object:
                Author.objects.filter(authorid=i).delete()

        return render(request, 'databaseauthor.html', {'object': all_obj})


@login_required
def author_update(request, pk):
    if request.user.is_authenticated:
        all_object = Author.objects.get(pk=pk)
        if request.method == 'POST':
            author_id = request.POST.get('authorid', None)
            name = request.POST.get('name', None)
            city = request.POST.get('city', None)
            country = request.POST.get('country', None)
            # Unique constrains is missing
            if all_object.authorid == int(author_id):
                if all_object.name != name:
                    Author.objects.filter(pk=pk).update(name=name)
                if all_object.city != city:
                    Author.objects.filter(pk=pk).update(city=city)
                if all_object.country != country:
                    Author.objects.filter(pk=pk).update(country=country)
            elif all_object.authorid != int(author_id):
                if Author.objects.filter(authorid=author_id).exists():
                    messages.error(request, "Author id already exist")
                else:
                    Author.objects.filter(pk=pk).create(
                        authorid=author_id, name=name, city=city, country=country)
            return redirect('deleteauthor')
        return render(request, 'authorupdate.html', {'update': all_object})


@login_required
def delete_publisher(request):
    if request.user.is_authenticated:
        all_obj = Publisher.objects.all()
        if request.method == 'POST':
            all_object = request.POST.getlist('allcheck[]')
            for i in all_object:
                Publisher.objects.filter(publisherid=i).delete()

        return render(request, 'deletepublisher.html', {'object': all_obj})


@login_required
def update_publisher(request, pk):
    if request.user.is_authenticated:
        all_object = Publisher.objects.get(pk=pk)
        if request.method == 'POST':
            publisher_id = request.POST.get('publisherid', None)
            name = request.POST.get('name', None)
            city = request.POST.get('city', None)
            country = request.POST.get('country', None)
            if Publisher.objects.filter(name=name).exists():
                messages.error(request,
                               "Publisher name already exist,Please give different one and try again")
            elif all_object.publisherid != int(publisher_id):
                if Publisher.objects.filter(publisherid=publisher_id).exists():
                    messages.error(request,
                                   "Publisher id already exist,Please give different one and try again")
                else:
                    Publisher.objects.filter(pk=pk).create(
                        publisherid=publisher_id, name=name, city=city, country=country)

            elif all_object.publisherid == int(publisher_id):
                if all_object.name != name:
                    Publisher.objects.filter(pk=pk).update(name=name)
                if all_object.city != city:
                    Publisher.objects.filter(pk=pk).update(city=city)
                if all_object.country != country:
                    Publisher.objects.filter(pk=pk).update(country=country)
            return redirect('deletepublisher')
        return render(request, 'updatepublisher.html', {'update': all_object})


@login_required
def delete_catagory(request):
    if request.user.is_authenticated:
        all_obj = Catagory.objects.all()
        if request.method == 'POST':
            all_object = request.POST.getlist('allcheck[]')
            for i in all_object:
                Catagory.objects.filter(catagoryid=i).delete()

        return render(request, 'deletecatagory.html', {'object': all_obj})


@login_required
def update_catagory(request, pk):
    if request.user.is_authenticated:
        all_object = Catagory.objects.get(pk=pk)
        if request.method == 'POST':
            Catagory_id = request.POST.get('catagoryid', None)
            description = request.POST.get('description', None)
            if all_object.catagoryid != int(Catagory_id):
                if Catagory.objects.filter(catagoryid=Catagory_id).exists():
                    messages.error(request,
                                   "Catagory id already exist,Please give different one and try again")
                else:
                    Catagory.objects.filter(pk=pk).create(
                        catagoryid=Catagory_id, description=description)

            elif all_object.catagoryid == int(Catagory_id):
                if all_object.description != description:
                    Catagory.objects.filter(pk=pk).update(
                        description=description)
            return redirect('deletecatagory')
        return render(request, 'updatecatagory.html', {'update': all_object})


@login_required
def delete_orderdetails(request):
    if request.user.is_authenticated:
        all_obj = Orderdetails.objects.all()
        if request.method == 'POST':
            all_object = request.POST.getlist('allcheck[]')
            for i in all_object:
                Orderdetails.objects.filter(orderno=i).delete()

        return render(request, 'deleteorderdetails.html', {'object': all_obj})


@login_required
def update_orderdetails(request, pk):
    if request.user.is_authenticated:
        all_object = Orderdetails.objects.get(pk=pk)
        all_values = Catalog.objects.all()
        if request.method == 'POST':

            order_no = request.POST.get('orderno', None)
            quantity = request.POST.get('quantity', None)
            book_id = request.POST['allvalue']
            if all_object.orderno != int(order_no) and book_id != " ":
                if Orderdetails.objects.filter(orderno=order_no).exists():
                    messages.error(request,
                                   "Order No already exist,Please give different one and try again")
                else:
                    t = Catalog.objects.get(pk=book_id)
                    Orderdetails.objects.filter(pk=pk).create(
                        orderno=order_no, quantity=quantity, bookid=t)

            elif all_object.orderno == int(order_no) and book_id != " ":
                if all_object.quantity != int(quantity):
                    Orderdetails.objects.filter(pk=pk).update(
                        quantity=int(quantity))
                if all_object.bookid != book_id:
                    Orderdetails.objects.filter(pk=pk).update(
                        bookid=book_id)

            elif all_object.orderno != int(order_no) and book_id == " ":
                if Orderdetails.objects.filter(orderno=order_no).exists():
                    messages.error(request,
                                   "Order No already exist,Please give different one and try again")
                else:
                    Orderdetails.objects.filter(pk=pk).create(
                        orderno=order_no, quantity=quantity, bookid=all_object.bookid)
            elif all_object.orderno == int(order_no) and book_id == " ":
                if all_object.quantity != int(quantity):
                    Orderdetails.objects.filter(pk=pk).update(
                        quantity=int(quantity))
            return redirect('deleteorderdetails')
        return render(request, 'updateorderdetails.html', {'update': all_object, 'values': all_values})


@login_required
def delete_catalog(request):
    if request.user.is_authenticated:
        all_obj = Catalog.objects.all()
        if request.method == 'POST':
            all_object = request.POST.getlist('allcheck[]')
            for i in all_object:
                Catalog.objects.filter(bookid=i).delete()

        return render(request, 'deletecatalog.html', {'object': all_obj})


@login_required
def update_catalog(request, pk):
    if request.user.is_authenticated:
        all_object = Catalog.objects.get(pk=pk)
        all_author = Author.objects.all()
        all_publisher = Publisher.objects.all()
        all_catagory = Catagory.objects.all()
        if request.method == 'POST':
            book_id = request.POST.get('bookid', None)
            title = request.POST.get('title', None)
            year_of_publish = request.POST.get('yearofpublish', None)
            price = request.POST.get('price', None)
            author_id = request.POST.get('allauthor', None)
            publisher_id = request.POST.get('allpublisher', None)
            catagory_id = request.POST.get('allcatagory', None)
            print(author_id)
            print(publisher_id)
            if all_object.bookid != int(book_id) and author_id != " " and publisher_id != " " and catagory_id != " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=author_id)
                    u = Publisher.objects.get(pk=publisher_id)
                    v = Catagory.objects.get(pk=catagory_id)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)
            elif all_object.bookid != int(book_id) and author_id != " " and publisher_id == " " and catagory_id == " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=author_id)
                    u = Publisher.objects.get(
                        pk=all_object.publisherid.publisherid)
                    v = Catagory.objects.get(
                        pk=all_object.catagoryid.catagoryid)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id != " " and publisher_id != " " and catagory_id == " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=author_id)
                    u = Publisher.objects.get(pk=publisher_id)
                    v = Catagory.objects.get(
                        pk=all_object.catagoryid.catagoryid)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id != " " and publisher_id == " " and catagory_id != " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=author_id)
                    u = Publisher.objects.get(
                        pk=all_object.publisherid.publisherid)
                    v = Catagory.objects.get(pk=catagory_id)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id == " " and publisher_id != " " and catagory_id != " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=all_object.authorid.authorid)
                    u = Publisher.objects.get(pk=publisher_id)
                    v = Catagory.objects.get(pk=catagory_id)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id == " " and publisher_id != " " and catagory_id == " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=all_object.authorid.authorid)
                    u = Publisher.objects.get(pk=publisher_id)
                    v = Catagory.objects.get(
                        pk=all_object.catagoryid.catagoryid)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id == " " and publisher_id == " " and catagory_id != " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=all_object.authorid.authorid)
                    u = Publisher.objects.get(
                        pk=all_object.publisherid.publisherid)
                    v = Catagory.objects.get(pk=catagory_id)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid != int(book_id) and author_id == " " and publisher_id == " " and catagory_id == " ":
                if Catalog.objects.filter(bookid=book_id).exists():
                    messages.error(request,
                                   "Book id already exist,Please give different one and try again")
                else:
                    t = Author.objects.get(pk=all_object.authorid.authorid)
                    u = Publisher.objects.get(
                        pk=all_object.publisherid.publisherid)
                    v = Catagory.objects.get(
                        pk=all_object.catagoryid.catagoryid)
                    Catalog.objects.filter(pk=pk).create(
                        bookid=book_id, title=title, year_of_publish=year_of_publish, price=price, authorid=t, publisherid=u, catagoryid=v)

            elif all_object.bookid == int(book_id) and author_id != " " and publisher_id != " " and catagory_id != " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(authorid=author_id)
                Catalog.objects.filter(pk=pk).update(publisherid=publisher_id)
                Catalog.objects.filter(pk=pk).update(catagoryid=catagory_id)

            elif all_object.bookid == int(book_id) and author_id != " " and publisher_id != " " and catagory_id == " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(authorid=author_id)
                Catalog.objects.filter(pk=pk).update(publisherid=publisher_id)

            elif all_object.bookid == int(book_id) and author_id != " " and publisher_id == " " and catagory_id != " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(authorid=author_id)
                Catalog.objects.filter(pk=pk).update(catagoryid=catagory_id)

            elif all_object.bookid == int(book_id) and author_id != " " and publisher_id == " " and catagory_id == " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(authorid=author_id)

            elif all_object.bookid == int(book_id) and author_id == " " and publisher_id != " " and catagory_id != " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(publisherid=publisher_id)
                Catalog.objects.filter(pk=pk).update(catagoryid=catagory_id)

            elif all_object.bookid == int(book_id) and author_id == " " and publisher_id != " " and catagory_id == " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(publisherid=publisher_id)

            elif all_object.bookid == int(book_id) and author_id == " " and publisher_id == " " and catagory_id != " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(catagoryid=catagory_id)

            elif all_object.bookid == int(book_id) and author_id == " " and publisher_id == " " and catagory_id == " ":
                Catalog.objects.filter(pk=pk).update(title=title)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)
                Catalog.objects.filter(pk=pk).update(price=price)
                Catalog.objects.filter(pk=pk).update(
                    year_of_publish=year_of_publish)

            return redirect('deletecatalog')
        return render(request, 'updatecatalog.html', {'update': all_object, 'author': all_author, 'publisher': all_publisher, 'catagory': all_catagory})
