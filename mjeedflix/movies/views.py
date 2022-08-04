from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status

from .models import Movies , Reviewes
from .serializers import ReviewesSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_movie (request : Request):
    
    user = request.user

    if not user.is_authenticated:
        return Response({"msg" : "Please Log In"})
    
    if not user.has_perm('movie.add_movie'):
        return Response({"msg" : "Sorry only admin can add movies"}, status=status.HTTP_401_UNAUTHORIZED)

    name = request.data["name"]
    genre = request.data["genre"]
    rating = request.data["rating"]
    release_date = request.data["release_date"]

    new_book = Movies(movie_name=name, genre=genre, rating=rating , release_date=release_date)
    new_book.save()

    res_data = {
            "msg" : "Created movie Successfully"
        }

    return Response(res_data)

@api_view(["GET"])
def list_all_movies(request: Request ):

    all_movies = Movies.objects.all()

    all_movies_list = [{"id" : movie.id, "movie_name" : movie.movie_name,"genre" : movie.genre, "rating" : movie.rating , "release_date" : movie.release_date} for movie in all_movies]

    res = {
        "msg" : "Movies",
        "movies" : all_movies_list
    }

    return Response(res, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_movie(request : Request, movie_id):
    
    user = request.user

    if not user.is_authenticated:
        return Response({"msg" : "Please Log In"})
    
    if not user.has_perm('movie.add_movie'):
        return Response({"msg" : "Sorry you don't have permission to update a movie"}, status=status.HTTP_401_UNAUTHORIZED)


    name = request.data["name"]
    genre = request.data["genre"]
    rating = request.data["rating"]
    release_date = request.data["release_date"]

    movie = Movies.objects.get(id=movie_id)

    movie.movie_name = name
    movie.genre = genre
    movie.rating = rating
    movie.release_date = release_date

    movie.save()

    return Response({"msg" : "Your movie is updated !"})


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_movie(request : Request, movie_id):
    
    user = request.user

    if not user.is_authenticated:
        return Response({"msg" : "Please Log In"})
    
    if not user.has_perm('movie.add_movie'):
        return Response({"msg" : "Sorry you don't have permission to update a movie"}, status=status.HTTP_401_UNAUTHORIZED)



    try:
        movie = Movies.objects.get(id=movie_id)
        movie.delete()
    except Exception as e:
        return Response({"msg" : "Sorry the movie is not Found"} , status=status.HTTP_404_NOT_FOUND)

    return Response({"msg" : f"delete the following movie {movie.movie_name }"})





@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request : Request):

    user_id = request.user.id

    request.data["user"] = user_id

    reviewes_serializer = ReviewesSerializer(data=request.data)

    if reviewes_serializer.is_valid():
        reviewes_serializer.save()
    else:
        return Response({"msg" : "couldn't create a review", "errors" : reviewes_serializer.errors}, status=status.HTTP_403_FORBIDDEN)

    
    return Response({"msg" : "Review Added Successfully!"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def list_reviews(request : Request):

    if "movie_id" in request.query_params:
        reviewes = Reviewes.objects.filter(movie=request.query_params["movie_id"])
    else:
        reviews = Reviewes.objects.all()

    reviews_data = ReviewesSerializer(instance=reviews, many=True).data

    return Response({"msg" : "list of all reviews", "review" : reviews_data })


@api_view(['PUT'])
def update_review(request : Request, review_id):

    try:
        reviewe = Reviewes.objects.get(id=review_id)
    except Exception as e:
        return Response({"msg" : "This review is not found"}, status=status.HTTP_404_NOT_FOUND)
    
    reviewes_serializer = ReviewesSerializer(instance=reviewe, data=request.data)

    if ReviewesSerializer.is_valid():
        ReviewesSerializer.save()
    else:
        return Response({"msg" : "couldn't update", "errors" :  reviewes_serializer.errors})

    return Response({"msg" : "Review updated successfully"})