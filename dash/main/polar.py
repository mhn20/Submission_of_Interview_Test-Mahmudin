import pandas as pd
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connections
from sqlalchemy import create_engine


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SQL():

    @classmethod
    def get_objects(self, q, using, vars, like=None):

        if not vars:
            with connections[using].cursor() as cursor:
                cursor.execute(q, vars)
                row = dictfetchall(cursor)
        else:
            with connections[using].cursor() as cursor:
                cursor.execute(q, vars)
                row = dictfetchall(cursor)

        return row

    @classmethod
    def call_procedure(self, name, using, params):
        """
        USAGE EXAMPLE
        --------------------------------------------------------------------------
        from main.polar import SQL
        SQL.call_procedure('TRANSFER_POLDA', 'hr_dalsdmdb', [202112,'060010100KD', '2022-04-15'])

        >>> True
        --------------------------------------------------------------------------
        """

        if not params:
            with connections[using].cursor() as cursor:
                try:
                    output = cursor.callproc(name, [])
                except:
                    output = False
        else:
            with connections[using].cursor() as cursor:
                try:
                    output = cursor.callproc(name, params)
                except:
                    output = False

        return output

    @classmethod
    def get_objects_with_pandas(self, q, using=None, vars=None, chunksize=None):

        if using:
            engine = "oracle://{}:InfoPers2019#@10.101.216.2:1521/{}".format(using.split('_')[0],
                                                                             using.split('_')[0])
        else:
            engine = create_engine(settings.SQL_ALCHEMY_ENGINE)

        if not chunksize:
            if not vars:
                d = pd.read_sql(q, engine)
            else:
                d = pd.read_sql(q, engine, params=vars)
        else:
            if not vars:
                d = pd.read_sql(q, engine, chunksize=chunksize)
            else:
                d = pd.read_sql(q, engine, params=vars, chunksize=chunksize)

        return d

    @classmethod
    def paginationRaw(self, request, dataset):

        limit = int(request.GET.get('limit', 25))
        paginator = Paginator(dataset, limit)

        json_data = []

        try:
            page = int(request.GET.get('page', 1))

            page_obj = paginator.page(page)

            data_page_range = []
            if page_obj.number > 3:
                for row_page_range in range(page_obj.number-1, page_obj.number+2):
                    if row_page_range <= page_obj.paginator.num_pages:
                        data_page_range.append(row_page_range)
            else:
                for row_page_range in range(1, 4):
                    if row_page_range <= page_obj.paginator.num_pages:
                        data_page_range.append(row_page_range)

            next_page = None
            if page_obj.has_next():
                next_page = page_obj.next_page_number()

            previous_page = None
            if page_obj.has_previous():
                previous_page = page_obj.previous_page_number()

            count_data = page_obj.paginator.count
            total_page = int(count_data/limit)
            if total_page <= 0:
                total_page = 1

            if page == 1:
                no = 0
            else:
                no = limit*(page-1)

            for rowindex in page_obj:
                no = no+1
                rowindex['NO'] = no
                json_data.append(rowindex)

            object_json = {
                'count': count_data,
                'total_page': page_obj.paginator.num_pages,
                'next': next_page,
                'paginator': {
                    'num_pages': page_obj.paginator.num_pages,
                    'page_range': data_page_range
                },
                'previous': previous_page,
                'page': page,
                'results': json_data
            }

        except Exception as e:

            page = 1

            page_obj = paginator.get_page(page)
            count_data = page_obj.paginator.count
            total_page = round(count_data/limit)
            if total_page <= 0:
                total_page = 1

            object_json = {
                'messages': str(e),
                'count': page_obj.paginator.count,
                'total_page': total_page,
                'next': None,
                'paginator': {
                    'num_pages': total_page,
                    'page_range': [1]
                },
                'previous': page,
                'page': page,
                'results': []
            }

        return object_json
