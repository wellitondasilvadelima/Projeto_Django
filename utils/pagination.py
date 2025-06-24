import math
from django.core.paginator import Paginator

def make_pagination_range(
        page_range ,
        qnt_pages,
        current_page,
):
    middle_range = math.ceil(qnt_pages/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if(start_range < 0) else 0

    if(start_range < 0):
        start_range = 0
        stop_range += start_range_offset
    
    if (stop_range >= total_pages):
        start_range = start_range  - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return{
        'pagination': pagination,
        'page_range': page_range,
        'qnt_pages': qnt_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range <total_pages,

    }

def make_pagination(request, queryset, per_page, qnt_page=4):
     try:
          current_page = int(request.GET.get('page',1))
     except ValueError:
          current_page = 1

     paginator = Paginator( queryset, per_page)
     page_obj = paginator.get_page(current_page)

     pagination_range = make_pagination_range(
          paginator.page_range,
          qnt_page,
          current_page,
     )
     return page_obj,pagination_range
    # before = math.floor(qnt_pages/2)
    # after = math.ceil(qnt_pages/2)
    # page_index  = page_range.index(current_page)
    # last_position = len(page_range)

    # if(page_index<=1):
    #     list_range = page_range[0:4]
    # else:
    #     list_range = page_range[page_index-before:page_index+after]

    # if(list_range.index(current_page)==2 and 
    #    page_index+after <= last_position-1 ):
        
    #     list_range = page_range[page_index-(before-1):page_index+(after+1)]
    # else:
    #     list_range = page_range[last_position-qnt_pages:last_position]

    # return list_range