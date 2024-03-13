from collections import namedtuple
from types import MappingProxyType

from license_plate_table.models import License_plate
from utilities.api_ai_query.ai_query import ai_query


def get_columns() -> list:
    return [column.name for column in License_plate._meta.get_fields()
            if column.name != 'id']


def init_dict_requests(request) -> dict:
    search_request = namedtuple('search', 'string_search func_search')
    dict_search_inputs = MappingProxyType(
        {'search_query':
             search_request(request.GET.get('query_search', None),
                            lambda search, objs: objs.raw(ai_query(search))),
         'search_license_name':
             search_request(request.GET.get('search_license_name', None),
                            lambda search, objs: objs.filter(license_plate=search), ),
         'selected_region':
             search_request(request.GET.get('select_region', None),
                            lambda search, objs: objs.filter(region=search), ),
         'start_date':
             search_request(request.GET.get('start_date', None),
                            lambda search, objs: objs.filter(date_time__date__gte=search), ),
         'end_date':
             search_request(request.GET.get('end_date', None),
                            lambda search, objs: objs.filter(date_time__date__lte=search), ),
         'user_name':
             search_request(request.GET.get('user_name', None),
                            lambda search, objs: objs.filter(user_name=search), ),
         'select_source':
             search_request(request.GET.get('select_source', None),
                            lambda search, objs: objs.filter(source=search), )
         })
    return dict_search_inputs
