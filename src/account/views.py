from django.http import HttpResponse
from django.shortcuts import render # noqa


def smoke(request):
    return HttpResponse('Hello i am account')
