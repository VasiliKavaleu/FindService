from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pg_records(request, list, num):
    paginator = Paginator(list, num)
    page = request.GET.get('page')
    try:
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)

    is_qs_paginated = page_object.has_other_pages()
    if page_object.has_previous():
        prev_page = f"&page={page_object.previous_page_number()}"
    else:
        prev_page = ""
    if page_object.has_next():
        next_page = f"&page={page_object.next_page_number()}"
    else:
        next_page = ""
    context = {}
    if page_object:
        context = {
            'is_qs_paginated' : is_qs_paginated,
            'next_page': next_page,
            'prev_page': prev_page,
            'autos': page_object,
            'city': page_object[0].city,
            'carModel': page_object[0].carModel
        }
    return context