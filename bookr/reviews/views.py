from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from .models import Book, Publisher, BookContributor
from .services import getting_books_list_from_db, getting_book_from_db, getting_reviews_list_from_db




def book_list(request):
    """
    Представление для отображения списка книг с возможностью поиска.
    
    Поддерживает поиск по:
    - названию книги
    - издательству
    - авторам/участникам
    """

    # Инициализация формы поиска с данными из GET-запроса
    form = SearchForm(request.GET or None)
    
    #Получение списка книг из базы данных
    book_list = getting_books_list_from_db(request)
    
    # Возврат шаблона с данными
    return render(request, 'reviews/book_list.html', {
        'book_list': book_list, 
        'form': form, 
    })


def book_details(request, pk):
    """
    Представление для отображения детальной информации о книге.
    
    Args:
        request: HTTP-запрос
        pk: Первичный ключ книги
    """

    # Получение книги по первичному ключу или возврат 404 ошибки
    book = getting_book_from_db(pk)
    #Получение списка отзывов из базы данных
    reviews_list = getting_reviews_list_from_db(book)
 
    # Возврат шаблона с данными книги и отзывами
    return render(request, 'reviews/book_detail.html', {
        'reviews': reviews_list, 
        'book': book
    })

