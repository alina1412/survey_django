from django.urls import path

from . import views


app_name = 'survey'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('add-survey/', views.AddSurveyView.as_view(), name='add_survey'),
    path('survey-detail/<int:pk>/', views.DetailSurveyView.as_view(), name='survey_detail'),
    path('surveys/', views.OwnedListSurveysView.as_view(), name='survey_list'),

    path('add-question/<int:survey_id>/', views.AddQuestionView.as_view(), name='add_question'),
    path('question-detail/<int:question_id>/', views.DetailQuestionView.as_view(), name="question_detail"),
    # path('question-list/', views.ListQuestionsView.as_view(), name='question_list'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SurveyLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-choice/<int:question_id>/', views.AddChoiceView.as_view(), name='add_choice'),
    path('answer/<int:survey_id>/', views.VotedAnswerView.as_view(), name='answer'),
    path('to-pass/', views.SurveyToPassView.as_view(), name="surveys_to_pass"),
    path('results/<int:survey_id>/', views.ResultsView.as_view(), name='results'),

]
