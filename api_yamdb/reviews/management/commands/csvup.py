import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre, Category, Comment, Title, GenreTitle, Review
from users.models import User


class Command(BaseCommand):
    help = 'CSV uploads'

    def handle(self, *args, **options):
        try:
            with open(
                'static/data/category.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    Category.objects.create(
                        id=i['id'],
                        name=i['name'],
                        slug=i['slug']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "Category" уже существуют'
            ))

        try:
            with open(
                'static/data/genre.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    Genre.objects.create(
                        id=i['id'],
                        name=i['name'],
                        slug=i['slug']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "Genre" уже существуют'
            ))

        try:
            with open(
                'static/data/users.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    User.objects.create(
                        id=i['id'],
                        username=i['username'],
                        email=i['email'],
                        role=i['role'],
                        bio=i['bio'],
                        first_name=i['first_name']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "User" уже существуют'
            ))

        try:
            with open(
                'static/data/titles.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    Title.objects.create(
                        id=i['id'],
                        name=i['name'],
                        year=i['year'],
                        category_id=i['category']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "Title" уже существуют'
            ))

        try:
            with open(
                'static/data/genre_title.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    GenreTitle.objects.create(
                        id=i['id'],
                        title_id=i['title_id'],
                        genre_id=i['genre_id']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "GenreTitle" уже существуют'
            ))

        try:
            with open(
                'static/data/review.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    Review.objects.create(
                        id=i['id'],
                        title_id=i['title_id'],
                        author_id=i['author'],
                        score=i['score'],
                        pub_date=i['pub_date'],
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "Review" уже существуют'
            ))

        try:
            with open(
                'static/data/comments.csv',
                'r',
                encoding='utf8',
            ) as csvfile:
                file_csv = csv.DictReader(csvfile)
                for i in file_csv:
                    Comment.objects.create(
                        id=i['id'],
                        reviews_id=i['review_id'],
                        text=i['text'],
                        author_id=i['author'],
                        pub_date=i['pub_date']
                    )
        except Exception:
            self.stdout.write(self.style.WARNING(
                'Такие данные в таблице "Comment" уже существуют'
            ))
