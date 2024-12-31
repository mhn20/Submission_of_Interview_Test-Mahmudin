import requests
from django.conf import settings
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from main.pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web.models import Movie
from web.serializers.movie_serializer import MovieSerializer


def index(request):
    template_name = 'page/list_movie.html'
    context = {'page_title': 'Movie Listings @ GV Cinema'}
    return render(request, template_name, context)


def detailMovie(request, idxrow):
    context = {'page_title': 'Movie Listings @ GV Cinema'}
    dataset = Movie.objects.filter(idxrow=idxrow).first()
    if dataset:
        template_name = 'page/detail_movie.html'
        context['dataset'] = dataset
    else:
        template_name = 'page/list_movie.html'
    return render(request, template_name, context)


@api_view(['GET'])
def listMovie(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 2)

    dataset = Movie.objects.order_by('-userRating', '-duration')

    search = request.GET.get('search')
    if search:
        dataset = dataset.filter(
            Q(name__icontains=search) | Q(description__icontains=search))

    paginator = CustomPageNumberPagination()
    pg = paginator.paginate_queryset(dataset, request)
    serializer_class = MovieSerializer(pg, many=True)
    serializer = paginator.get_paginated_response(serializer_class.data)

    return JsonResponse(serializer.data)
