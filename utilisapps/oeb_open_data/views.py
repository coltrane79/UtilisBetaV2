from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def oeb_open_data(request):
    try:
        return render(request, "oeb_open_data/open_data.html")
    except Exception as ex:
        print(ex)
