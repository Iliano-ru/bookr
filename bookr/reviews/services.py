from django.shortcuts import get_object_or_404
from .models import Book, BookContributor

def _getting_data_from_request(request):
     # Получение параметров поиска из GET-запроса
    request_get = request.GET
    search = request_get.get('search')  # Поисковый запрос
    title_checkbox = request_get.get('title')  # Флажок поиска по названию
    publisher_checkbox = request_get.get('publisher')  # Флажок поиска по издательству
    contributors_checkbox = request_get.get('contributors')  # Флажок поиска по участникам
    return search, title_checkbox, publisher_checkbox, contributors_checkbox


def getting_books_list_from_db(request):
    search, title_checkbox, publisher_checkbox, contributors_checkbox = _getting_data_from_request(request)

    # Инициализация пустого списка для результатов поиска
    book_list = []
    
    # Логика поиска: если есть поисковый запрос И выбран хотя бы один флажок
    if search and (title_checkbox or publisher_checkbox or contributors_checkbox):
        # Поиск по участникам (авторам, редакторам и т.д.)
        if contributors_checkbox:
            contributors = BookContributor.objects.all()
            for contributor in contributors:
                # Проверка, содержит ли имя участника поисковый запрос (без учета регистра)
                if search.lower() in contributor.contributor.full_name.lower():
                    book_list.append(contributor.book)
        
        # Поиск по названию книги (без учета регистра)
        if title_checkbox:
            book_list.extend(Book.objects.filter(title__icontains=search))
            
        # Поиск по названию издательства (без учета регистра)
        if publisher_checkbox:
            book_list.extend(Book.objects.filter(publisher__name__icontains=search))
            
    # Если поисковый запрос пустой, показываем все книги
    elif not search:
        book_list = Book.objects.all()

    return book_list


def getting_book_from_db(pk):
    return get_object_or_404(Book, pk=pk)


def getting_reviews_list_from_db(book):
    return book.review_set.all()
    