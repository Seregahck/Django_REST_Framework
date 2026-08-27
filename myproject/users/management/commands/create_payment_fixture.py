from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from users.models import Payment
from decimal import Decimal
import json
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Создает фикстуру для модели Payment'

    def handle(self, *args, **options):
        User = get_user_model()

        # Получаем или создаем пользователей
        users = User.objects.all()
        if not users.exists():
            self.stdout.write('Создаем тестовых пользователей...')
            for i in range(1, 6):
                User.objects.create_user(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password='testpass123'
                )
            users = User.objects.all()

        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if not courses.exists():
            self.stdout.write('Создаем тестовые курсы...')
            for i in range(1, 4):
                course = Course.objects.create(
                    title=f'Тестовый курс {i}',
                    description=f'Описание тестового курса {i}'
                )
                for j in range(1, 4):
                    Lesson.objects.create(
                        course=course,
                        title=f'Урок {j} курса {i}',
                        description=f'Описание урока {j}'
                    )
            courses = Course.objects.all()
            lessons = Lesson.objects.all()

        # Создаем платежи
        self.stdout.write('Создаем платежи...')
        payments = []
        for user in users:
            for _ in range(random.randint(1, 4)):
                payment_data = {
                    'user': user.id,
                    'payment_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                    'amount': str(Decimal(random.randint(100, 5000)) / 100),
                    'payment_method': random.choice(['cash', 'transfer']),
                }

                # Случайно выбираем оплату курса или урока
                if random.choice([True, False]):
                    if courses.exists():
                        payment_data['paid_course'] = random.choice(courses).id
                else:
                    if lessons.exists():
                        payment_data['paid_lesson'] = random.choice(lessons).id

                # Проверяем, что заполнено хотя бы одно поле
                if 'paid_course' not in payment_data and 'paid_lesson' not in payment_data:
                    if courses.exists():
                        payment_data['paid_course'] = random.choice(courses).id

                payments.append(payment_data)

        # Сохраняем в файл
        with open('users/fixtures/payments.json', 'w', encoding='utf-8') as f:
            json.dump(payments, f, indent=2, ensure_ascii=False, default=str)

        self.stdout.write(self.style.SUCCESS('Фикстура создана: users/fixtures/payments.json'))

        # Загружаем фикстуру
        self.stdout.write('Загружаем фикстуру...')
        from django.core.management import call_command
        call_command('loaddata', 'users/fixtures/payments.json')
        self.stdout.write(self.style.SUCCESS('Фикстура успешно загружена!'))
