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
from .models import Book, Review, Author
from .serializers import BookSerializer, ReviewSerializer, AuthorSerializer
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

    # @transaction.atomic
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


# class BookUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = Book.objects.filter(is_active=True)
#     serializer_class = BookSerializer
#     lookup_field = 'id'

#     @transaction.atomic
#     def update(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()

#             # Extract author data from the request
#             author_data = request.data.pop('author', None)

#             # If author data is provided, check if the author exists
#             if author_data:
#                 author_id = author_data.get('id')
#                 if author_id:
#                     author_instance = Author.objects.get(pk=author_id)
#                     author_serializer = AuthorSerializer(instance=author_instance, data=author_data)
#                 else:
#                     author_serializer = AuthorSerializer(data=author_data)

#                 author_serializer.is_valid(raise_exception=True)
#                 author = author_serializer.save()
#                 instance.author = author

#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#         except Exception as e:
#             transaction.set_rollback(True)
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data)
    
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
            return Response(serializer.data)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class BookSoftDeleteRestoreView(generics.RetrieveUpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     lookup_field = 'id'

#     @transaction.atomic
#     def update(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             # instance = self.get_object()
            
#             # Set the is_active field based on the request data
#             is_active = request.data.get('is_active', not instance.is_active)
#             request.data['is_active'] = is_active
#             print(request.data['is_active'] )

#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
#         except Exception as e:
#             transaction.set_rollback(True)
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # @cache_page(60 * 15)  # Cache for 15 minutes
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)