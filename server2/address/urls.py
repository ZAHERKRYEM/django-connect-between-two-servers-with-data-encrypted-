from django.urls import path
from . import views

urlpatterns = [
    path('personal/<str:national_id>', views.PersonalDataView.as_view()),

]
