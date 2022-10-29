menu_notlog = [
    {"url_name": "survey_app:home", "descr": "home"},
    {"url_name": "survey_app:login", "descr": "login"},
    {"url_name": "survey_app:register", "descr": "register"},
]
menu = [
    {"url_name": "survey_app:surveys_to_pass", "descr": "surveys to pass"},
]

menu_log = [
    {"url_name": "survey_app:survey_list", "descr": "your survey's list"},
    {
        "url_name": "survey_app:logout",
        "descr": "logout",
        "onclick": "return myFunction();",
    },
]


def get_menu(request):
    if request.user.is_authenticated:
        return menu + menu_log
    return menu_notlog + menu
