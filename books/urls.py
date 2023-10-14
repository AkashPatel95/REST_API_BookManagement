from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='home'),
    path('create/', views.add_book, name='add-book'),
    path('all/', views.view_books, name='view_books'),
    path('update/<int:pk>/', views.update_book, name='update-book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete-book'),
    # Additional paths for other API endpoints can be added here
]
