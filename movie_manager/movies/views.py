from django.contrib import messages
from django.shortcuts import render
from . models import movieinfo
from . form import movieForm
from .resources import MovieInfoResource
from tablib import Dataset
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse

def create(request):
    frm = movieForm()

    if request.method == "POST":
        title = request.POST.get('title', '').strip().upper()
        year = int(request.POST.get('year'))
        description = request.POST.get('description', '').strip().upper()

        exists = movieinfo.objects.filter(
            title=title,
            year=year,
           
        ).exists()

        if exists:
            messages.error(request, " This movie already exists!")
        else:
            movieinfo.objects.create(
                title=title,
                year=year,
                description=description
            )
            messages.success(request, " Movie added successfully!")

        
        movieSet = movieinfo.objects.all()
        return render(request, 'list.html', {'movie': movieSet})

    return render(request, 'index.html', {'frm': frm})


def list(request):
    movie_set = movieinfo.objects.all() 
   
    print(movie_set)
    return render(request, 'list.html', {'movie': movie_set})

def edit (request,pk):
    instance=movieinfo.objects.get(pk=pk)
    print(instance)
    if request.method == "POST":  
        title = request.POST.get('title').strip().upper()
        year = request.POST.get('year')
        desc = request.POST.get('description').strip().upper()
        exists = movieinfo.objects.filter(
            title=title,
            year=year,
           
        ).exists()
        if exists:
            messages.error(request, " This movie details already exists!")
        else:
            messages.success(request, " Movie edit successfully!")
        instance.title=title
        instance.year=year
        instance.description=desc
        instance.save()
        
        instance=movieinfo.objects.all() 
        return render(request, 'list.html',{'movie':instance})
    
       
    
def delete(request, pk):
    instance = movieinfo.objects.get(pk=pk)
    title = instance.title  
    instance.delete()
    messages.success(request, f"Movie '{title}' deleted successfully.")
    movie_set = movieinfo.objects.all()
    return render(request, 'list.html', {'movie': movie_set})



# def impor(request):
#     if request.method == "POST":
#         movieinfo=MovieInfoResource()
#         dataset=dataset()
#         update=request.files['myfile']
#         fulldata=dataset.load(update.read())
#     return render(request, 'edit.html')


# def impor(request):
#     if request.method == "POST":
#         movieinfo_resource = MovieInfoResource()
#         dataset = Dataset()

#         new_file = request.FILES['myfile']
#         imported_data = dataset.load(new_file.read(), format='xlsx')

#         result = movieinfo_resource.import_data(dataset, dry_run=True)

#         if not result.has_errors():
#             movieinfo_resource.import_data(dataset, dry_run=False)

#     movieSet = movieinfo.objects.all()
#     return render(request, 'list.html', {'movie': movieSet})




def impor(request):
    if request.method == "POST":
        new_file = request.FILES['myfile']
        df = pd.read_excel(new_file)

        added = 0
        skipped = 0

        for _, row in df.iterrows():
            title = str(row['title']).strip().upper()
            year = int(row['year'])
            description = str(row['description']).strip().upper()

            exists = movieinfo.objects.filter(
                title=title,
                year=year,
               
                
            ).exists()

            if exists:
                skipped += 1
            else:
                movieinfo.objects.create(
                    title=title,
                    year=year,
                    description=description,
                    
                )
                added += 1

        if added == 0:
            messages.error(request, "This file already exists! Nothing new was uploaded.")
        else:
            messages.success(request, f"{added} rows uploaded successfully!")
    movieSet = movieinfo.objects.all()
    return render(request, 'list.html', {'movie': movieSet})

def export_movieinfo(request):
    format = request.GET.get('format', 'csv') 

    qs = movieinfo.objects.all().values()
    df = pd.DataFrame.from_records(qs)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="movieinfo.csv"'
        df.to_csv(path_or_buf=response, index=False)

    elif format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="movieinfo.xlsx"'
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

    elif format == 'pdf':
        
        html = df.to_html(index=False)
        result = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="movieinfo.pdf"'
        response.write(result.getvalue())
    
    elif format == 'json':
        response = HttpResponse(df.to_json(orient='records'), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="movieinfo.json"'
        
    else:
        return HttpResponse('Invalid format', status=400)

    return response
