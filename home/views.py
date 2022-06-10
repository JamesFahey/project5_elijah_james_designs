from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def handel_404(request, exception):
    """View to return 404 error page if page does not exists"""

    return render(request, 'home/404.html')
