from django.urls import path

from .views import EmailValidationAPIView, LeadAPIView, PlayAPIView, LeadDetailAPIView

urlpatterns = [
    path("game/<str:emblem>", PlayAPIView.as_view()),
    path("leads", LeadAPIView.as_view()),
    path("leads/<str:emblem>", LeadDetailAPIView.as_view()),
    path("play/email_validation", EmailValidationAPIView.as_view()),
]
