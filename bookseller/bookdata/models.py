from django.db import models
from django.utils.timezone import timezone


class Author(models.Model):
    authorid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return (str(self.authorid) + '(' + self.name + ')')


class Publisher(models.Model):
    publisherid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return (str(self.publisherid) + '(' + self.name + ')')


class Catagory(models.Model):
    catagoryid = models.IntegerField(primary_key=True)
    description = models.TextField()

    def __str__(self):
        return (str(self.catagoryid) + '(' + self.description.split(' ', 1)[0] + ')')


class Catalog(models.Model):
    bookid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    year_of_publish = models.CharField(max_length=5)
    price = models.FloatField()
    authorid = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    publisherid = models.ForeignKey(
        'Publisher', on_delete=models.CASCADE, null=True)
    catagoryid = models.ForeignKey(
        'Catagory', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (str(self.bookid) + '(' + self.title + ')')


class Orderdetails(models.Model):
    orderno = models.IntegerField(primary_key=True)
    quantity = models.IntegerField(primary_key=False)
    bookid = models.ForeignKey(
        'Catalog', on_delete=models.CASCADE, db_column='bookid', null=True)

    def __str__(self):
        return str(self.orderno)
