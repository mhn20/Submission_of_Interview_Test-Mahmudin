import json

from django.conf import settings
from django.core.paginator import Paginator
from main.polar import SQL
from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = "limit"

    def get_paginated_response(self, data):

        if self.page.has_next():
            next_page_number = self.page.next_page_number()
        else:
            next_page_number = None

        if self.page.has_previous():
            previous_page_number = self.page.previous_page_number()
        else:
            previous_page_number = None

        data_page_range = []
        if self.page.number > 3:
            for row_page_range in range(self.page.number-1, self.page.number+2):
                if row_page_range <= self.page.paginator.num_pages:
                    data_page_range.append(row_page_range)
        else:
            for row_page_range in range(1, 4):
                if row_page_range <= self.page.paginator.num_pages:
                    data_page_range.append(row_page_range)

        if self.page.has_previous():
            first_page = 1
        else:
            first_page = None

        if self.page.has_next():
            last_page = self.page.paginator.num_pages
        else:
            last_page = None

        return Response({
            'start_index': self.page.start_index(),
            'first_page': first_page,
            'last_page': last_page,
            'paginator': {
                'num_pages': self.page.paginator.num_pages,
                'page_range': data_page_range
            },
            'number': self.page.number,
            'has_next': self.page.has_next(),
            'next_page_number': next_page_number,
            'has_previous': self.page.has_previous(),
            'previous_page_number': previous_page_number,
            'count': self.page.paginator.count,
            'results': data
        })


class CustomRawQueryPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"

    def paginate_queryset(self, raw_query, request, conn='hr_v3'):
        request.query_params = request.GET

        page_number = int(request.GET.get('page', 1))
        page_size = self.get_page_size(request)

        results = SQL.get_objects(raw_query, conn, {})
        paginator = Paginator(results, page_size)
        self.page = paginator.get_page(page_number)

        return self.page

    def get_paginated_response(self, data):

        if self.page.has_next():
            next_page_number = self.page.next_page_number()
        else:
            next_page_number = None

        if self.page.has_previous():
            previous_page_number = self.page.previous_page_number()
        else:
            previous_page_number = None

        data_page_range = []
        if self.page.number > 3:
            for row_page_range in range(self.page.number-1, self.page.number+2):
                if row_page_range <= self.page.paginator.num_pages:
                    data_page_range.append(row_page_range)
        else:
            for row_page_range in range(1, 4):
                if row_page_range <= self.page.paginator.num_pages:
                    data_page_range.append(row_page_range)

        if self.page.has_previous():
            first_page = 1
        else:
            first_page = None

        if self.page.has_next():
            last_page = self.page.paginator.num_pages
        else:
            last_page = None

        return Response({
            'start_index': self.page.start_index,
            'first_page': first_page,
            'last_page': last_page,
            'paginator': {
                'num_pages': self.page.paginator.num_pages,
                'page_range': data_page_range
            },
            'number': self.page.number,
            'has_next': self.page.has_next(),
            'next_page_number': next_page_number,
            'has_previous': self.page.has_previous(),
            'previous_page_number': previous_page_number,
            'count': self.page.paginator.count,
            'results': data
        })
