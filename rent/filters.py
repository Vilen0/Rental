import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='icontains', label='Марка')
    body_type = django_filters.ChoiceFilter(choices=Car.BODY_TYPES, label='Тип кузова')
    current_price = django_filters.RangeFilter(label='Цена (руб./день)')

    class Meta:
        model = Car
        fields = ['brand', 'body_type', 'current_price']