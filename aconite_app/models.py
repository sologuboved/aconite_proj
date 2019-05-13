from django.db import models


class Language(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Location(models.Model):
    ru_name = models.CharField()
    en_name = models.CharField()

    def __str__(self):
        return "{} / {}".format(self.ru_name, self.en_name)


class Person(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    ru_name = models.CharField()
    en_name = models.CharField()

    def __str__(self):
        return "{} / {}".format(self.ru_name, self.en_name)


class Category(models.Model):
    is_prose = models.BooleanField()
    genre = models.ManyToManyField(
        Genre,
    )

    def __str__(self):
        return "{} {}".format(type(self.is_prose), self.is_prose)
        # return "Is{}prose: {}".format({True: " ", False: " not "}[self.is_prose], self.genre)


class Content(models.Model):
    title = models.CharField()
    text = models.TextField()
    num_part = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    location = models.ManyToManyField(
        Location,
        null=True
    )
    language = models.ManyToManyField(
        Language,
        null=True
    )
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "{}:({}) {}".format(self.work, self.num_part, self.title)


class Work(models.Model):
    title = models.CharField()
    author = models.ManyToManyField(
        Person,
        null=True
    )
    # contents: reverse relation to Content

    def __str__(self):
        return "{} - {}".format(self.author, self.title)


class Inspiration(models.Model):
    pass



# category = models.ForeignKey(
#     Category,
#     on_delete=models.CASCADE,
#     null=True
# )


