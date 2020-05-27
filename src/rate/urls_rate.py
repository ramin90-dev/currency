from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('all/', views.rate_all, name='all'),
]