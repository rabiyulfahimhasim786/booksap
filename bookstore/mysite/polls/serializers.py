from rest_framework import serializers
from .models import Author, Book, Review

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)  # Set read_only=True

    class Meta:
        model = Book
        fields = '__all__'

    # def validate_isbn(self, value):
    #     """
    #     Validate that the ISBN is unique.
    #     """
    #     if Book.objects.filter(isbn=value).exists():
    #         raise serializers.ValidationError("ISBN must be unique.")
    #     return value
    # def create(self, validated_data):
    #     author_data = validated_data.pop('author')
    #     author_instance = Author.objects.create(**author_data)

    #     reviews_data = validated_data.pop('reviews', [])
    #     book_instance = Book.objects.create(author=author_instance, **validated_data)

    #     for review_data in reviews_data:
    #         Review.objects.create(book=book_instance, **review_data)

    #     return book_instance
   
    def validate_isbn(self, value):
        """
        Validate that the ISBN is unique.
        """
        existing_books = Book.objects.exclude(pk=getattr(self.instance, 'pk', None))
        if existing_books.filter(isbn=value).exists():
            raise serializers.ValidationError("ISBN must be unique.")
        return value

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_instance = Author.objects.create(**author_data)

        reviews_data = validated_data.pop('reviews', [])
        book_instance = Book.objects.create(author=author_instance, **validated_data)

        for review_data in reviews_data:
            Review.objects.create(book=book_instance, **review_data)

        return book_instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        author_data = validated_data.get('author', {})
        author_instance, created = Author.objects.get_or_create(**author_data)
        instance.author = author_instance

        instance.save()

        return instance 