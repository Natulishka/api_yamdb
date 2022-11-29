from django.db import models


# Категории
class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE,
        related_name="category"
    )

# Жанры
class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

# Произведения
class Titles(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    genre = models.ManyToManyField(Genres, through='GenresTitles')
        
    class Grade (models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

        grade = models.IntegerField(choices=Grade.choices)

    rating = models.IntegerField


    def __str__(self):
        return self.text
