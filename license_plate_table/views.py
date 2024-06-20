import django.db
from django.shortcuts import render
from license_plate_table.models import License_plate
from utilities.data_repr.column_func import get_columns, init_dict_requests
from profile_and_site_settings.models import WhiteList


def view_data_table(request):
    main_objs = License_plate.objects.all()
    white_list = WhiteList.objects.all()
    for item in main_objs:
        lic_plate = item.license_plate
        print("license", lic_plate)
        for item_white in white_list:
            print("white", item_white.license_plate)
            if item_white.license_plate == lic_plate:
                license_plate_obj = License_plate.objects.get(id=item.id)
                license_plate_obj.user_name = item_white.user_name
                license_plate_obj.save()
    main_objs = License_plate.objects.all()
    columns = get_columns()
    return render(
        request,
        "license_plate_table/license_plate_table.html",
        {"license_plate": main_objs, "columns": columns},
    )


def search_view(request):
    main_objs = License_plate.objects.all()
    columns = get_columns()
    if request.method == "GET":
        search_request = init_dict_requests(request)
        if string_query := search_request["search_query"].string_search:
            columns, main_objs = query_search(search_request, string_query, main_objs)
        else:
            main_objs = standart_search(main_objs, search_request)
    return render(
        request,
        "license_plate_table/license_plate_table.html",
        {"license_plate": main_objs, "columns": columns},
    )


def query_search(search_request, string_query, main_objs):
    try:
        main_objs = search_request["search_query"].func_search(string_query, main_objs)
        columns = [column for column in main_objs.columns if column != "id"]
    except django.db.utils.ProgrammingError:
        main_objs = License_plate.objects.all()
        columns = get_columns()
    return columns, main_objs


def standart_search(main_objs, search_request):
    searched_valid_input = dict(
        filter(
            lambda text_query: True if text_query[1].string_search else False,
            search_request.items(),
        )
    )
    for key in searched_valid_input:
        main_objs = searched_valid_input[key].func_search(
            searched_valid_input[key].string_search, main_objs
        )
    return main_objs
