menu_notlog = [
    {
        "url_name": 'survey_app:home',
        "descr": 'home'
    },
    {
        "url_name": 'survey_app:login',
        "descr": 'login'
    },
    {
        "url_name": 'survey_app:register',
        "descr": 'register'
    },

]
menu = [
    {
        "url_name": 'survey_app:surveys_to_pass',
        "descr": 'surveys to pass'
    },
]

menu_log = [
    {
        "url_name": 'survey_app:survey_list',
        "descr": "your survey's list"
    },
    # {  "url_name": 'survey_app:add_survey',
    #     "descr": 'add survey'
    # },
    {
        "url_name": 'survey_app:logout',
        "descr": 'logout',
        "onclick": "return myFunction();"
    },

]


def get_menu(request):
    if request.user.is_authenticated:
        return menu + menu_log
    return menu_notlog + menu


# menu_param = [
#     {  "url_name": '/survey_app/add_question/1',
#         "descr": 'add_question_to_the_first_survey'
#     },
#     {  "url_name": '/survey_app/add_choice/1',
#         "descr": 'add choice for1'
#     },
#     {  "url_name": '/survey_app/answer/1',
#         "descr": 'vote for s1'
#     },
#     {  "url_name": '/survey_app/question_detail/1',
#         "descr": 'question1'
#     },
#     {  "url_name": '/survey_app/survey_detail/1',
#         "descr": 'survey1'
#     },
# ]
