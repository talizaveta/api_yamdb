from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


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
    year = models.IntegerField(verbose_name='Год выхода'),
    genre = models.ManyToManyField(
        Genre,
        null=True,
        on_delete=models.SET_NULL,
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now=True)
