from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_courses',
        verbose_name='Владелец',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        permissions = [
            ('can_view_course', 'Может просматривать курсы'),
            ('can_change_course', 'Может изменять курсы'),
            ('can_delete_course', 'Может удалять курсы'),
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_lessons',
        verbose_name='Владелец',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        permissions = [
            ('can_view_lesson', 'Может просматривать уроки'),
            ('can_change_lesson', 'Может изменять уроки'),
            ('can_delete_lesson', 'Может удалять уроки'),
        ]

    def __str__(self):
        return self.title