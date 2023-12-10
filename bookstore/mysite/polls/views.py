from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from django.views.decorators.cache import cache_page
def index(request):
    return HttpResponse("Hello, world!")
from rest_framework import generics
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
#paginations
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'per_page'
    max_page_size = 100

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    pagination_class = CustomPageNumberPagination
    print(pagination_class)    
    # @cache_page(60 * 15)  # Cache for 15 minutes
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    lookup_field = 'id'


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    lookup_field = 'id'

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
    
class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)
        author = self.request.query_params.get('author', None)
        genre = self.request.query_params.get('genre', None)
        publication_year = self.request.query_params.get('publication_year', None)

        if author:
            queryset = queryset.filter(author__name__icontains=author)

        if genre:
            queryset = queryset.filter(author__genre=genre)
            # queryset = queryset.filter(genre__icontains=genre)

        if publication_year:
            # queryset = queryset.filter(publication_year=publication_year)
            queryset = queryset.filter(author__publication_year=publication_year)

        return queryset
    




class BookSoftDeleteRestoreView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = not instance.is_active
            instance.save()
            serializer = self.get_serializer(instance)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # @cache_page(60 * 15)  # Cache for 15 minutes
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)