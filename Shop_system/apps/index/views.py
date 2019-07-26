from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request,'index.html')