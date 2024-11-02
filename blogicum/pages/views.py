from django.shortcuts import render


def about(request):
    """Описание"""
    return render(request, 'pages/about.html')


def rules(request):
    """Правила"""
    return render(request, 'pages/rules.html')
