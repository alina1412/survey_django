from django.urls import path

from survey_app.views import views, views_choices_answers, views_questions, views_survey

app_name = "survey_app"
urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("add-survey/", views_survey.AddSurveyView.as_view(), name="add_survey"),
    path(
        "survey-detail/<int:survey_id>/",
        views_survey.DetailSurveyView.as_view(),
        name="survey_detail",
    ),
    path("surveys/", views_survey.OwnedListSurveysView.as_view(), name="survey_list"),
    path(
        "add-question/<int:survey_id>/",
        views_questions.AddQuestionView.as_view(),
        name="add_question",
    ),
    path(
        "question-detail/<int:question_id>/",
        views_questions.DetailQuestionView.as_view(),
        name="question_detail",
    ),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.SurveyLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "add-choice/<int:question_id>/",
        views_choices_answers.AddChoiceView.as_view(),
        name="add_choice",
    ),
    path(
        "answer/<int:survey_id>/",
        views_choices_answers.VotedAnswerView.as_view(),
        name="answer",
    ),
    path("to-pass/", views_survey.SurveyToPassView.as_view(), name="surveys_to_pass"),
    path(
        "results/<int:survey_id>/", views_survey.ResultsView.as_view(), name="results"
    ),
]
