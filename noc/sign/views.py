from django.shortcuts import render


def start_page(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'sign/login.html')
