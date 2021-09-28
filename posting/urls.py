from django.urls import path
from .views import (
    PostingView,
    PostingSearchView
)

urlpatterns = [
    path('/p', PostingView.as_view()),
    path('/search/<int:user_id>', PostingSearchView.as_view())
]
