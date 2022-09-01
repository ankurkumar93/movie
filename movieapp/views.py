from curses.ascii import US
from datetime import date
from re import M
from django.shortcuts import render
from rest_framework.views import APIView
import hashlib
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_jwt.settings import api_settings
import requests
from django.core.paginator import Paginator
import jwt, datetime
from movie import settings
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, AllowAny
from .methods import CheckUser


class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            username = serializer.data['username']
            password = serializer.data['password']
            hashedPassword = make_password(password)
            user = User.objects.create(username=username, password=hashedPassword)
            payload = {
                'id': user.id,
                'username': user.username
            }
            accessToken = jwt.encode(payload, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm='HS256')
            return Response({'access_token':accessToken}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

            
class MovieView(APIView):
    def get(self, request):
        try:
            page = request.GET.get('page')
            if not page:
                page = '1'
                dataUrl = 'https://demo.credy.in/api/v1/maya/movies/'
            else:
                dataUrl = 'https://demo.credy.in/api/v1/maya/movies/?page={}'.format(page)
        
            if int(page) < 1:
                return Response({'error':'Invalid page'})

            r = requests.get(dataUrl)
            movieList = {}
            movieDetails = {}
            dataDict = r.json()
            moviesList = dataDict['results']
            p = Paginator(moviesList, 10)
            page_data = p.get_page(page) 
            moviesList = page_data.__dict__['object_list'] 
            url = request.build_absolute_uri('/')
            if 'is_success' not in dataDict.keys():
                movieList['count'] = dataDict['count']
                movieList['next'] = url + 'movie?page=' + str(int(page) + 1)
                if page != 0:
                    movieList['previous'] = url + 'movie?page=' + str(int(page) - 1)
                if page == '1':
                    movieList['previous'] = None
                movieList['data'] = []

                for movie in moviesList:
                    movieDetails['title'] = movie['title']
                    movieDetails['description'] = movie['description']
                    movieDetails['genres'] = movie['genres']
                    movieDetails['uuid'] = movie['uuid']
                    movieList['data'].append(movieDetails)
                return Response(movieList)
            else:
                return Response({'message':'Please try again later'})
        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Collection(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user = CheckUser(token)
        if not user:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'User with that id not found'})
        else:
            dataDict = {}
            dataDict['is_success'] = True
            dataDict['data'] = {}
            dataDict['data']['collections'] = []
            movieDetail = {
                'title': 'Title of my collection',
                'uuid': 'uuid of the collection name',
                'description': 'My description of the collection.'
            }
            dataDict['data']['collections'].append(movieDetail)
            ################################# T O   D O #############################

            # # allCollectionMovies = MovieCollection.objects.prefetch_related('movies').filter(user=userid)
            # # favGenre = MovieCollection.objects.values('genre').order_by().annotate(Count('genre'))
            # allCollectionMovies = MovieCollection.movies.through.objects.all()
            # for collection in allCollectionMovies:
            #     names = Movie.objects.get(name=MovieCollection.objects.prefetch_related('movies').get(name=(collection.__dict__['movie_id'])))
            #     # print("sasasas", MovieCollection.objects.prefetch_related('movies').get(movies=(collection.__dict__['movie_id'])))
            #     print("fdfddf", names)

            ##########################################################################
            favGenre = 'horror'
            dataDict['data']['favourite_genres'] = favGenre
            return Response(dataDict)
            
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        serializer_class = AddCollectionSerializer
        user = CheckUser(token)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        userInstance = User.objects.get(username=user)
        try:
            collectionInstance = MovieCollection.objects.create(title=request.data['title'],
                description=request.data['description'], user=userInstance)
            for movie in request.data['movies']:
                movieInstance = Movie.objects.create(name=movie['title'], genre=movie['genre'])
                collectionInstance.movies.add(movieInstance.id)
        except Exception as ss:
            return Response(status=status.HTTP_400_BAD_REQUEST)              
        return Response({'collection_uuid': collectionInstance.id})


class EditCollection(APIView):

    def get(self, request, collection_uuid):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        CheckUser(token)
        try:
            collectionInstance = MovieCollection.objects.get(id=collection_uuid)
        except Exception as ee:
            return Response({'message':'Not found with that ID'}, status=status.HTTP_404_NOT_FOUND)
        dataDict = {}
        dataDict['title'] = collectionInstance.title
        dataDict['description'] = collectionInstance.description
        allMovies = MovieCollection.movies.through.objects.filter(moviecollection_id=collection_uuid).values()
        dataDict['movies'] = list(allMovies)
        return Response(dataDict, status=status.HTTP_200_OK)

    def put(self, request, collection_uuid, format=None):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user = CheckUser(token)
        if not user:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'User with that id not found'})
        try:
            collectionObject = MovieCollection.objects.filter(id=collection_uuid).update(title=request.data['title'], description=request.data['description'])
            collectionInstance = MovieCollection.objects.get(id=collection_uuid)

        except Exception as ee:
            return Response({'message':'Not found with that ID'}, status=status.HTTP_404_NOT_FOUND)

        for movie in request.data['movies']:
            movieInstance = Movie.objects.create(name=movie['title'], genre=movie['genre'])
            collectionInstance.movies.add(movieInstance.id)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, collection_uuid):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user = CheckUser(token)
        if not user:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'User with that id not found'})
        try:
            collectionObject = MovieCollection.objects.filter(id=collection_uuid).delete()
        except Exception as ee:
            return Response({'message':'Not found with that ID'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
        

class RequestCounter(APIView):

    def get(self,request):
        try:
            count = RequestCount.objects.values('count').first()['count']
            return Response({'requests':count}, status=status.HTTP_200_OK)
        except:
            return Response({'message':'Please try later'}, status=status.HTTP_400_BAD_REQUEST)


class ResetCounter(APIView):

    def put(self, request):
        try:
            RequestCount.objects.values('count').update(count=0)
            return Response({'message':'request count reset successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'message':'Please try later'}, status=status.HTTP_400_BAD_REQUEST)
        