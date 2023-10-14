from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import get_object_or_404  # Import the get_object_or_404 function
from .models import Book  # Import the Book model
from .serializers import BookSerializer

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'All Books': '/',
        'Search by Title': '/?title=title_name',
        'Search by Author': '/?author=author_name',
        'Add Book': '/create',
        'Update Book': '/update/pk',
        'Delete Book': '/book/pk/delete'
    }

    return Response(api_urls)

@api_view(['POST'])
def add_book(request):
    if request.method == 'POST':
        book_serializer = BookSerializer(data=request.data)

        # Check for existing data
        if Book.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This book already exists')

        if book_serializer.is_valid():
            book_serializer.save()
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def view_books(request):
    if request.query_params:
        books = Book.objects.filter(**request.query_params)
    else:
        books = Book.objects.all()

    if books:
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    book_serializer = BookSerializer(instance=book, data=request.data)

    if book_serializer.is_valid():
        book_serializer.save()
        return Response(book_serializer.data)
    else:
        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
