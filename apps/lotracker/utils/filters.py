from rest_framework.filters import SearchFilter


class CustomSearchFilter(SearchFilter):
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '%': 'icontains',
    }