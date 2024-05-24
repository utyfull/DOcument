import django_filters
from .models import UserFile


class fileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Title')
    uploaded_at = django_filters.OrderingFilter(
        fields=(
            ('uploaded_at', 'uploaded_at'),
        ),
        field_labels={
            'uploaded_at': 'Date',
        },
        label='Sort by'
    )

    class Meta:
        model=UserFile
        fields = ['name', 'uploaded_at']


class foreign_fileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(field_name='user', lookup_expr='icontains', label='Author')
    uploaded_at = django_filters.OrderingFilter(
        fields=(
            ('uploaded_at', 'uploaded_at'),
        ),
        field_labels={
            'uploaded_at': 'Date',
        },
        label='Sort by'
    )

    class Meta:
        model=UserFile
        fields = ['name', 'author', 'uploaded_at']