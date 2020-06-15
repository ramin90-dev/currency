from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('list/', views.RateList.as_view(), name='list'),
    path('edit/<int:pk>/', views.UpdateRate.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteRate.as_view(), name='delete'),
    path('download-csv/', views.RateDownloadCSV.as_view(), name='download-csv'),
    path('download-xlsx/', views.RateDownloadXLSX.as_view(), name='download-xlsx'),
    path('latest-rate/', views.LatestRatesView.as_view(), name='latest-rate'),

]
