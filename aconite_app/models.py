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
    ru_name = models.CharField(max_length=250, null=True, blank=True)
    en_name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return "{} / {}".format(self.ru_name, self.en_name)


class Genre(models.Model):
    ru_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    is_prose = models.NullBooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return "{} / {}; {}rosaic".format(self.ru_name, self.en_name, {True: 'p', False: 'non-p'}[self.is_prose])


class Content(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    dedication = models.CharField(max_length=1000, null=True, blank=True)
    text = models.TextField()
    num_part = models.IntegerField()
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return "{}:({}) {}".format(self.work, self.num_part, self.title)


class Book(models.Model):
    title = models.CharField(max_length=1000)
    authors = models.ManyToManyField(
        Person
    )
    languages = models.ManyToManyField(
        Language
    )

    def __str__(self):
        return "{} - {}".format(self.authors, self.title)


class Inspiration(Book):
    # works: reverse relation to Work

    def __str__(self):
        return "{} - {}".format(self.authors, self.title)


class Work(Book):
    original_title = models.CharField(max_length=1000, null=True, blank=True)
    dedication = models.CharField(max_length=1000, null=True, blank=True)
    year_demo = models.CharField(max_length=250, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    locations = models.ManyToManyField(
        Location
    )
    is_translation = models.BooleanField()
    inspirations = models.ManyToManyField(
        Inspiration
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # contents: reverse relation to Content

    def __str__(self):
        return "{} - {}".format(self.authors, self.title)
