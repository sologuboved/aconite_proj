from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Location(models.Model):
    ru_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} / {}".format(self.ru_name, self.en_name)


class Person(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Genre(models.Model):
    ru_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} / {}".format(self.ru_name, self.en_name)


class Category(models.Model):
    is_prose = models.BooleanField()
    genres = models.ManyToManyField(
        Genre
    )

    def __str__(self):
        return "{} {}".format(type(self.is_prose), self.is_prose)
        # return "{}rosaic: {}".format({True: "P, False: "Non-p"}[self.is_prose], self.genre)


class Content(models.Model):
    title = models.CharField(max_length=3000)
    text = models.TextField()
    num_part = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    locations = models.ManyToManyField(
        Location
    )
    languages = models.ManyToManyField(
        Language
    )
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "{}:({}) {}".format(self.work, self.num_part, self.title)


class Book(models.Model):
    title = models.CharField(max_length=3000)
    author = models.ManyToManyField(
        Person
    )

    def __str__(self):
        return "{} - {}".format(self.author, self.title)


class Inspiration(Book):
    # works: reverse relation to Work

    def __str__(self):
        return "{} - {}".format(self.author, self.title)


class Work(Book):
    is_translation = models.BooleanField()
    inspirations = models.ManyToManyField(
        Inspiration
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    # contents: reverse relation to Content

    def __str__(self):
        return "{} - {}".format(self.author, self.title)
