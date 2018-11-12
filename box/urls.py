from django.urls import path
from .views.boxview import BoxView

urlpatterns = [
    path('', BoxView.as_view())
]