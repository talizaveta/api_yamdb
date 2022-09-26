import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb import settings
from reviews.models import (
    Categories, Genres, Title, GenreTitle, Review, Comment)
from users.models import User

path = f'{settings.BASE_DIR}/static/data/'
os.chdir(path)

TABLES = {
    'users': User,
    'category': Categories,
    'genre': Genres,
    'titles': Title,
    'genre_title': GenreTitle,
    'review': Review,
    'comments': Comment,
}


class Command(BaseCommand):
    help = 'Команда для импорта данных в БД из csv-файла.'

    def handle(self, *args, **options):
        for file_name, model in TABLES.items():
            with open(f'{file_name}.csv') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')

                if file_name == 'titles':
                    for row in reader:
                        category = Categories.objects.get(
                            pk=row.pop('category')
                        )
                        obj = model(
                            category=category,
                            **row
                        )
                        obj.save()

                elif file_name in ['review', 'comments']:
                    for row in reader:
                        author = User.objects.get(pk=row.pop('author'))
                        obj = model(
                            author=author,
                            **row
                        )
                        obj.save()

                else:
                    model.objects.bulk_create(
                        [model(**row) for row in reader]
                    )

                print('Данные загружены')
