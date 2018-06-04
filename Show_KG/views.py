from django.shortcuts import render
from django.shortcuts import HttpResponse
from Show_KG.Load.LoadNeo import kg_service
from Show_KG.Load import LoadNer
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')
def splash(request):
    return render(request,'splash.html')
def query_brother(request):
    return HttpResponse(kg_service.query_brother_node())

def query_brother(request):
    return HttpResponse(kg_service.query_brother_node())
def query_super(requst):
    return HttpResponse(kg_service.query_super_node())
def query_cooperation(requst):
    return HttpResponse(kg_service.query_cooperation_node())
def ner(request):
    text = None
    if request.method == 'POST':
        text = request.POST.get('text','')
    if request.method == 'GET':
        text = "我是艾成铭"
    return HttpResponse(json.dumps(LoadNer.ner(text),ensure_ascii=False))

def ner_page(request):
    return render(request,'ner.html')

def query_brother_page(request):
    return render(request,'query_brother.html')

def query_cooperation_page(request):
    return render(request,'query_cooperation.html')

def query_super_page(request):
    return render(request,'query_super.html')
def re_page(request):
    return render(request,'re_page.html')