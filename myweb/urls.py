from django.urls import path
from . import views
from .views import SurveyView, AddAnswersView  # Import the class-based views
from .views import edit_submitted_data

urlpatterns = [
    
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),

    path('signout/', views.signout, name='signout'),
    path('forgotpwd/', views.forgotpwd, name='forgotpwd'),
    path('activate/<uidb64><tokens>', views.activate, name='activate'),
    path('survey_form/', views.survey_form, name='survey_form'),

    path('new_question/', views.new_question, name='new_question'),
     path('survey/', SurveyView.as_view(), name='survey'),
    path('add_answers/<int:question_id>/', AddAnswersView.as_view(), name='add_answers'),
    path('edit-submitted-data/', edit_submitted_data, name='edit_submitted_data'),  # Add new URL pattern

]
