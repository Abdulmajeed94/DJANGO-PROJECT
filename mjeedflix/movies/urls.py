from django.urls import path
from . import views 

urlpatterns = [
    
    path('add/' , views.add_movie , name='add_movie'),
    path("all/", views.list_all_movies, name="list_movies"),
    path("update/<movie_id>/", views.update_movie, name="update_movie"),
    path("delete/<movie_id>/", views.delete_movie, name="delete_movie"),
    #Reviewers
    path("reviews/add/", views.add_review, name="add_review"),
    path("reviews/all/", views.list_reviews, name="list_all_reviews"),
    path("reviews/update/<review_id>/", views.update_review, name="update_review")
    
]
