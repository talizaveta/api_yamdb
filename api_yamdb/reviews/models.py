from django.db import models


class Category(models.Model):
    """Модель для создания категорий."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название категории',
        help_text='Введите название категории'
    ),
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес',
        help_text='Адрес категории должен быть уникальным'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Модель для создания жанров."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название жанра',
        help_text='Введите название категории'
    ),
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес',
        help_text='Адрес жанра должен быть уникальным'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    """Модель для создания произведения."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Введите название произведения'
    ),
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
        help_text='Введите описание произведения'
    )
    year = models.IntegerField(verbose_name='Дата выхода'),
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    ),
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Жанр'
    ),
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']
