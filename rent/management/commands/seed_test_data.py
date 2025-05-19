from django.core.management.base import BaseCommand
from rent.models import CarModel, Car, Booking
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = "Создаёт тестовые данные: пользователей, модели авто, автомобили, бронирования"

    def handle(self, *args, **kwargs):
        # Пользователь
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('testpassword')
            user.save()

        # Модели автомобилей
        car_models = [
            {'brand': 'Toyota', 'model': 'Corolla', 'body_type': 'sedan'},
            {'brand': 'Honda', 'model': 'CR-V', 'body_type': 'suv'},
            {'brand': 'Volkswagen', 'model': 'Golf', 'body_type': 'hatchback'},
            {'brand': 'Kia', 'model': 'Carnival', 'body_type': 'minivan'},
        ]

        car_model_instances = []
        for data in car_models:
            cm, _ = CarModel.objects.get_or_create(**data)
            car_model_instances.append(cm)

        # Автомобили
        locations = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург']
        transmissions = ['auto', 'manual']
        fuel_types = ['petrol', 'diesel', 'electric']

        car_instances = []
        for cm in car_model_instances:
            for i in range(2):  # По 2 машины каждой модели
                car = Car.objects.create(
                    car_model=cm,
                    year=random.randint(2015, 2023),
                    transmission=random.choice(transmissions),
                    fuel_type=random.choice(fuel_types),
                    min_price=1500,
                    max_price=5000,
                    current_price=random.randint(2000, 4000),
                    location=random.choice(locations),
                    status='available',
                )
                car_instances.append(car)

        # Бронирования
        for car in car_instances:
            for i in range(2):  # По 2 бронирования
                start_date = timezone.now().date() - timedelta(days=random.randint(5, 25))
                end_date = start_date + timedelta(days=random.randint(1, 7))
                Booking.objects.create(
                    car=car,
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=car.current_price * (end_date - start_date).days,
                    status='confirmed'
                )

        self.stdout.write(self.style.SUCCESS("✅ Тестовые данные успешно созданы!"))
