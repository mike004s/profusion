from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Databases
# Create your views here.
@login_required(login_url='/login')
def home (request):
    return render(request, 'index.html')


def home(request):
     if request.method =='POST':
        names = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        data =Databases(name=names, email=email, phone=phone, message=message)
        data.save()
     return render(request, 'index.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')  
        if name and email and message:  
            Databases.objects.create(name=name, email=email, message=message)
            return render(request, 'success.html')
        else:
            return render(request, 'contact.html', {'error': 'All fields are required.'})
    return render(request, 'contact.html')



def database(request):
    data = Databases.objects.all()
    context ={
        'data': data
    }
    return render(request, 'database.html', context)




def update(request, id):
    updateInfo = Databases.objects.get(id=id)
    
    if request.method == 'POST':
        updateInfo.name = request.POST.get('name')
        updateInfo.email = request.POST.get('email')
        updateInfo.phone = request.POST.get('phone')
        updateInfo.message = request.POST.get('message')
        updateInfo.save()
        return redirect('database')
    context = {
        'updateInfo': updateInfo
    }
    return render(request, 'update.html',context)




# def home(request):
#     profile = None
#     if request.user.is_authenticated:
#         profile = request.user.profile

#     return render(request, 'home.html', {'profile': profile})
