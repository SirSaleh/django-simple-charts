from django.urls import path
from . import views

urlpatterns = [
    path('sample-charts/', views.ChartsSampleView.as_view())
]