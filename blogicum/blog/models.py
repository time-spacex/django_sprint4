from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel


MAX_CHAR_LENGTH = 256
MAX_CLASS_STRING_LENGTH = 20


User = get_user_model()


class Category(PublishedModel):
    """Модель содержит категории постов."""

    title = models.CharField('Заголовок', max_length=MAX_CHAR_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:MAX_CLASS_STRING_LENGTH]


class Location(PublishedModel):
    """Модель содержит локацию для публикации."""

    name = models.CharField(
        'Название места',
        max_length=MAX_CHAR_LENGTH,
        default='Планета Земля'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_CLASS_STRING_LENGTH]


class Post(PublishedModel):
    """Модель для публикации постов."""

    title = models.CharField('Заголовок', max_length=MAX_CHAR_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now=False,
        auto_now_add=False,
        help_text='Если установить дату и время в будущем — можно делать '
                  'отложенные публикации.'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts_images',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:MAX_CLASS_STRING_LENGTH]


class Comment(PublishedModel):
    """Класс для добавления комментариев к постам"""

    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (f'{str(self.id)} {self.author.username} '
        f'{self.text}')[:MAX_CLASS_STRING_LENGTH]
