from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает группу модераторов с правами на просмотр и редактирование курсов и уроков'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='moderators')

        if created:
            self.stdout.write('Группа модераторов создана')
        else:
            self.stdout.write('Группа модераторов уже существует')

        # Получаем content types для моделей
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        # Список разрешенных действий для модераторов (без создания и удаления)
        allowed_permissions = ['view', 'change']
        # Запрещенные действия
        denied_permissions = ['add', 'delete']

        # Получаем разрешения для курсов
        course_permissions = Permission.objects.filter(
            content_type=course_content_type,
            codename__in=[f'{action}_course' for action in allowed_permissions]
        )

        # Получаем разрешения для уроков
        lesson_permissions = Permission.objects.filter(
            content_type=lesson_content_type,
            codename__in=[f'{action}_lesson' for action in allowed_permissions]
        )

        # Добавляем разрешения группе
        moderator_group.permissions.set(list(course_permissions) + list(lesson_permissions))

        self.stdout.write(self.style.SUCCESS(
            f'Группе модераторов добавлены разрешения: '
            f'{len(course_permissions) + len(lesson_permissions)} разрешений'
        ))

        # Выводим информацию о разрешениях
        self.stdout.write('Разрешения модераторов:')
        for perm in moderator_group.permissions.all():
            self.stdout.write(f'  - {perm.codename}')
