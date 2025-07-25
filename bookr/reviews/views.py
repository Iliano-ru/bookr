from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from .models import Book
from .utils import average_rating
from django.db.models import Q

def index(request):
    return render(request, 'base.html')

def book_list(request):
    # Объвление формы
    form = SearchForm(request.GET or None)

    search = request.GET.get('search')

    if search != None:
        # Фильтрация книг по заголовку
        book_list = Book.objects.filter(Q(title__icontains=search) | Q(publisher__name__icontains=search))
    else:
        book_list = Book.objects.all()


    # Расчет среднего рейтинга и количества отзывов для каждой книги
    for book in book_list:
        rating_list = []
        reviews_list = book.review_set.all()
        for review in reviews_list:
            rating_list.append(review.rating)
        setattr(book, 'average_rating', average_rating(rating_list))
        # book.average_rating = average_rating(rating_list)
        book.reviews_count = len(reviews_list)

    
    return render(request, 'reviews/book_list.html', {'book_list': book_list, 'form': form, 'search': search})

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    rating_list = []
    reviews_list = book.review_set.all()
    for review in reviews_list:
        rating_list.append(review.rating)
    setattr(book, 'average_rating', average_rating(rating_list))
    return render(request, 'reviews/book_detail.html', {'reviews': reviews_list, 'book':book})