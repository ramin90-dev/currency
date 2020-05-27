from django.shortcuts import render

from rate.models import Rate


def rate_all(request):
    rate = Rate.objects.all()
    count = rate.count()
    return render(request, 'list_all.html', context={'rates': rate,
                                                       'count': count
                                                       }
                  )