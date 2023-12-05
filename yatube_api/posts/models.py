from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
SYMBOLS_COUNT = 25


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title[:SYMBOLS_COUNT]


class Post(models.Model):
    text = models.TextField('Заголовок')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True,
        verbose_name='Группа'
    )
    ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:SYMBOLS_COUNT]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField('Заголовок')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:SYMBOLS_COUNT]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='following',
        blank=True, null=True,
        verbose_name='Подписка'
    )

    class Meta:
        """
        - Проверка составной уникальности в UniqueConstraint
        - Ограничение подписки на самого себя в CheckConstraint
        """

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
            models.CheckConstraint(
                name='cant_subscribe_to_yourself',
                check=~models.Q(user=models.F('following')),
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.following}'
