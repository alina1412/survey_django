
from django.urls import path

from . import views


app_name = 'survey'
urlpatterns = [
    path('', views.home_view, name='h'),
    path('add-survey/', views.AddSurveyView.as_view(), name='add_survey'),
    path('survey-detail/<int:pk>/', views.DetailSurveyView.as_view(), name='survey_detail'),
    path('surveys/', views.ListSurveysView.as_view(), name='survey_list'),

    path('add-question/<int:survey_id>/', views.AddQuestionView.as_view(), name='add_question'),
    path('question-detail/<int:pk>/', views.DetailQuestionView.as_view(), name="question_detail"),
    # path('question-list/', views.ListQuestionsView.as_view(), name='question_list'),

    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    path('add-choice/<int:question_id>/', views.AddChoiceView.as_view(), name='add_choice'),
    path('answer/<int:survey_id>/', views.VotedAnswerView.as_view(), name='answer')
    

]


