from django.shortcuts import render, get_object_or_404

from .models import Book
from .utils import average_rating

def index(request):
    return render(request, 'base.html')

def book_list(request):
    book_list = Book.objects.all()
    for book in book_list:
        rating_list = []
        reviews_list = book.review_set.all()
        for review in reviews_list:
            rating_list.append(review.rating)
        setattr(book, 'average_rating', average_rating(rating_list))
        # book.average_rating = average_rating(rating_list)
        book.reviews_count = len(reviews_list)
    return render(request, 'reviews/book_list.html', {'book_list': book_list})

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    rating_list = []
    reviews_list = book.review_set.all()
    for review in reviews_list:
        rating_list.append(review.rating)
    setattr(book, 'average_rating', average_rating(rating_list))
    return render(request, 'reviews/book_detail.html', {'reviews': reviews_list, 'book':book})