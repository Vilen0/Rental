from django.core.management.base import BaseCommand
from rent.models import Car
from math import log
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates car prices based on occupied days (D) and idle days (S)'

    def handle(self, *args, **kwargs):
        # Параметры
        D_max = 30  # Максимум занятых дней
        S_max = 30  # Максимум дней простоя
        w_D = 0.7   # Вес занятых дней
        w_S = 0.3   # Вес простоя
        max_price_change = Decimal('200.00')  # Ограничение ±200 руб./день

        for car in Car.objects.all():
            try:
                # Получить D и S
                D = car.occupied_days
                S = car.idle_days

                # Нормировка с логарифмом
                Z_D_norm = log(D + 1) / log(D_max + 1)
                Z_S_norm = 1 - log(S + 1) / log(S_max + 1)

                # Индекс спроса
                demand = w_D * Z_D_norm + w_S * Z_S_norm

                # Рассчитать новую цену
                middle_price = (car.min_price + car.max_price) / 2
                price_range = (car.max_price - car.min_price) / 2
                demand_factor = Decimal(str(2 * demand - 1))  # Преобразовать float в Decimal
                new_price = middle_price + price_range * demand_factor

                # Ограничить цену диапазоном min_price–max_price
                new_price = max(car.min_price, min(car.max_price, new_price))

                # Ограничить изменение ±100 руб.
                if car.current_price is not None:
                    new_price = max(
                        car.current_price - max_price_change,
                        min(car.current_price + max_price_change, new_price)
                    )
                else:
                    # Если current_price не установлена, использовать middle_price
                    new_price = middle_price

                # Округлить до 2 знаков
                #new_price = new_price.quantize(Decimal('0.01'))

                # Округлить до ближайших 50 рублей
                new_price = (new_price / 50).quantize(Decimal('1'), rounding='ROUND_HALF_UP') * 50

                # Обновить цену, если изменилась
                if car.current_price != new_price:
                    old_price = car.current_price
                    car.current_price = new_price
                    car.save(update_fields=['current_price'])
                    logger.info(
                        f'Updated price for {car}: D={D}, S={S}, '
                        f'demand={demand:.2f}, old_price={old_price}, new_price={new_price}'
                    )
                else:
                    logger.debug(f'No price change for {car}: current_price={car.current_price}')

            except Exception as e:
                logger.error(f'Error updating price for {car}: {str(e)}', exc_info=True)

        self.stdout.write(self.style.SUCCESS('Successfully updated car prices'))