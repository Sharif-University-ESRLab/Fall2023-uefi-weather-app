from django.urls import path

from demo.views import DemoAPIView

urlpatterns = [
    path('weather', DemoAPIView.as_view()),
]
