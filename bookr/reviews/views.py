from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from .models import Book, Publisher, BookContributor
from .utils import average_rating



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
    
    # Получение параметров поиска из GET-запроса
    request = request.GET
    search = request.get('search')  # Поисковый запрос
    title_checkbox = request.get('title')  # Флажок поиска по названию
    publisher_checkbox = request.get('publisher')  # Флажок поиска по издательству
    contributors_checkbox = request.get('contributors')  # Флажок поиска по участникам
    
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

    # Расчет дополнительных данных для каждой книги
    for book in book_list:
        rating_list = []  # Список для хранения рейтингов
        reviews_list = book.review_set.all()  # Получение всех отзывов для книги
        
        # Сбор всех рейтингов из отзывов
        for review in reviews_list:
            rating_list.append(review.rating)
        
        # Добавление среднего рейтинга как атрибута книги
        setattr(book, 'average_rating', average_rating(rating_list))
        
        # Добавление количества отзывов как атрибута книги
        book.reviews_count = len(reviews_list)

    # Возврат шаблона с данными
    return render(request, 'reviews/book_list.html', {
        'book_list': book_list, 
        'form': form, 
        'search': search
    })

def book_details(request, pk):
    """
    Представление для отображения детальной информации о книге.
    
    Args:
        request: HTTP-запрос
        pk: Первичный ключ книги
    """
    # Получение книги по первичному ключу или возврат 404 ошибки
    book = get_object_or_404(Book, pk=pk)
    
    # Расчет среднего рейтинга для книги
    rating_list = []  # Список для хранения рейтингов
    reviews_list = book.review_set.all()  # Получение всех отзывов для книги
    
    # Сбор всех рейтингов из отзывов
    for review in reviews_list:
        rating_list.append(review.rating)
    
    # Добавление среднего рейтинга как атрибута книги
    setattr(book, 'average_rating', average_rating(rating_list))
    
    # Возврат шаблона с данными книги и отзывами
    return render(request, 'reviews/book_detail.html', {
        'reviews': reviews_list, 
        'book': book
    })

