import django_filters
from django.db.models import Q
from .models import Car, Booking, CarModel
from django.forms.widgets import DateInput
from datetime import date


class CarFilter(django_filters.FilterSet):
    brand = django_filters.ChoiceFilter(
        field_name='car_model__brand',
        choices=lambda: [(brand, brand) for brand in CarModel.objects.values_list('brand', flat=True).distinct()],
        label='Марка'
    )
    body_type = django_filters.ChoiceFilter(field_name='car_model__body_type', choices=CarModel.BODY_TYPES,
                                            label='Тип кузова')
    current_price = django_filters.RangeFilter(label='Цена (руб./день)')
    start_date = django_filters.DateFilter(method='filter_by_date', label='Дата начала',
                                           widget=DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateFilter(method='filter_by_date', label='Дата окончания',
                                         widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Car
        fields = ['brand', 'body_type', 'current_price']

    def filter_by_date(self, queryset, name, value):
        start_date = self.form.cleaned_data.get('start_date')
        end_date = self.form.cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                return queryset.none()  # Неверные даты
            if start_date < date.today():
                return queryset.none()  # Даты в прошлом

            # Исключаем авто с пересекающимися бронированиями
            booked_cars = Booking.objects.filter(
                status__in=['confirmed', 'pending'],
                start_date__lte=end_date,
                end_date__gte=start_date
            ).values_list('car_id', flat=True)

            queryset = queryset.exclude(id__in=booked_cars)

        return queryset