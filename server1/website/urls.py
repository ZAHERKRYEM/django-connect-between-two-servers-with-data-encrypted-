from django.urls import path
from .import views
urlpatterns = [

    path('personal/<int:id>', views.personal,name='personal'),

]