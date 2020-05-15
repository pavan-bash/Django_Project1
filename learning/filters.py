import django_filters
from django_filters import DateFilter

from .models import *

class BlogFilter(django_filters.FilterSet):
	after_date = DateFilter(field_name='date_posted', lookup_expr='gte')
	class Meta:
		model = Post
		fields = {'title': ['icontains', ], 'category': ['icontains', ]}

class CourseFilter(django_filters.FilterSet):
	class Meta:
		model = Course
		fields = {'name': ['icontains', ]}
