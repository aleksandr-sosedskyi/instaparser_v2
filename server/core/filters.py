import operator

from functools import reduce
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.db.models import Q

from core.models import InstaUser, BlackListWords


class GoodUsersFilter(SimpleListFilter):
    title = 'Good users'
    parameter_name = 'users'

    def lookups(self, request, model_admin):
        return (
            ('good', 'good'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'good':
            return queryset.filter(
                ~Q(email=None) &
                reduce(operator.and_, (~Q(username__icontains=x) for x in BlackListWords.objects.values_list('word', flat=True))),
                status=InstaUser.RIGHT_EMAIL
            )
        return queryset
