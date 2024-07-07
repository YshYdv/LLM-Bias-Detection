
from django.urls import path
from violenceDetection.views import InputTextViewSet

urlpatterns = [
    path('', InputTextViewSet.as_view(), name='viol')
]
