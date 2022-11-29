from django.http import Http404
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    # 添加会话的支持
    num_visited = request.session.get('num_visited', 0)
    request.session['num_visited'] = num_visited + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
                'num_instances':num_instances,
                'num_instances_available':num_instances_available,
                'num_visited': num_visited,
                'num_authors':num_authors},
    )
# 返回图书列表
# def books(request):
#     book_list = Book.objects.all().get()

#     return render(
#         request,
#         book_list.html,
#         context=(
#             book_list
#         )
#     )

class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location
    # 添加翻页支持
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

    template_name = 'book_detail.html'  # Specify your own template name/location

    # 如果记录不存，抛出404异常，同时返回book id
    # def book_detail_view(request,pk):
    #     try:
    #         book_id=Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         raise Http404("Book does not exist")

    #     #book_id=get_object_or_404(Book, pk=pk)

    #     return render(
    #         request,
    #         'catalog/book_detail.html',
    #         context={'book':book_id,}
    #     )

class AuthorListView(generic.ListView):
    model = Author

    template_name = 'author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author

    template_name = 'author_detail.html'

