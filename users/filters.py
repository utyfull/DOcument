import django_filters
from .models import UserFile


class fileFilter(django_filters.FilterSet):
    name1 = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Title')
    uploaded_at1 = django_filters.OrderingFilter(
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
        fields = ['name1', 'uploaded_at1']


class foreign_fileFilter(django_filters.FilterSet):
    name2 = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Title')
    author2 = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='Author')
    uploaded_at2 = django_filters.OrderingFilter(
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
        fields = ['name2', 'author2', 'uploaded_at2']