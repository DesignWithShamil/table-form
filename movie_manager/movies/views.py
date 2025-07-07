
from django.shortcuts import render
from . models import movieinfo
from . form import movieForm



def create(request):
    frm=movieForm()
    if request.method == "POST":  # Always better than just `if request.POST`
        title = request.POST.get('title')
        year = request.POST.get('year')
        desc = request.POST.get('description')

        movie_obj = movieinfo(title=title, year=year, description=desc)
        movie_obj.save()
        movieSet=movieinfo.objects.all()
        return render(request, 'list.html', {'movie':movieSet})
    return render(request, 'create.html',{'frm':frm})

def list(request):
    movie_set = movieinfo.objects.all() 
   
    print(movie_set)
    return render(request, 'list.html', {'movie': movie_set})

def edit (request,pk):
    instance=movieinfo.objects.get(pk=pk)
    print(instance)
    if request.method == "POST":  # Always better than just `if request.POST`
        title = request.POST.get('title')
        year = request.POST.get('year')
        desc = request.POST.get('description')
        instance.title=title
        instance.year=year
        instance.description=desc
        instance.save()
        instance=movieinfo.objects.all() 
        return render(request, 'list.html',{'movie':instance})
    
def delete(request,pk):
    instance=movieinfo.objects.get(pk=pk)
    instance.delete()
    movie_set = movieinfo.objects.all() 
    return render(request, 'list.html', {'movie': movie_set})


def add(request):
   
    if request.method == "POST":  # Always better than just `if request.POST`
        title = request.POST.get('title')
        year = request.POST.get('year')
        desc = request.POST.get('description')

        movie_obj = movieinfo(title=title, year=year, description=desc)
        movie_obj.save()
        
    movieSet=movieinfo.objects.all()
    return render(request, 'list.html', {'movie':movieSet})