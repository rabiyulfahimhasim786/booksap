from django.urls import path
from. import views
from .views import BookListCreateView, BookRetrieveUpdateDeleteView, BookListView,BookUpdateView, ReviewListCreateView,BookSoftDeleteRestoreView


urlpatterns = [
    path("index/", views.index, name="index"),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:id>/', BookRetrieveUpdateDeleteView.as_view(), name='book-retrieve-update-delete'),
    path('books/<int:id>/delete/', BookSoftDeleteRestoreView.as_view(), name='book-delete-restore'),
    path('books/list/', BookListView.as_view(), name='book-list'),
    path('books/<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/reviews/', ReviewListCreateView.as_view,name='reveiew-list-create'),
]