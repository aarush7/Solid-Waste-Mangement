from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,WasteGenerationForm,LfGenerationForm,PpGenerationForm,TvGenerationForm,TvUpdateForm,LfUpdateForm,PpUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import TUser,Waste,ProcesssingPlant,TransportVehicle,Landfill,WasteML
import csv

from django.http import HttpResponse

def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Date', 'Waste'])

    for member in WasteML.objects.all().values_list('date', 'waste_qty'):
        writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="waste.csv"'

    return response

def mlscript():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from pathlib import Path
    import os
    import seaborn as sns
    BASE_DIR = Path(__file__).resolve().parent.parent
    path=os.path.join(BASE_DIR,'invt/dataset/waste.csv')
    
    df=pd.read_csv(path)
    df.sort_values(by=['Date'],axis=0,inplace=True)
    last=df.tail(1)['Date']
    
    
    df=df.dropna()
    import datetime as dt
    def convert_date_to_ordinal(date):
        t=dt.datetime.strptime(str(date),'%Y-%M-%d').date()
        return t.toordinal()
    df['Date']=df['Date'].apply(convert_date_to_ordinal)
    X=df[['Date']]
    y=df[['Waste']]

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=101)

    from sklearn.linear_model import LinearRegression
    lm= LinearRegression()
    lm.fit(X_train,y_train)
    from sklearn import metrics
    import datetime
    r=str(last).split('\n')
    r1=r[0].split(' ')
    r2=r1[4].split('-')
    dt = datetime.datetime(int(r2[0]), int(r2[1]), int(r2[2]))
    end = datetime.datetime(int(r2[0])+2, int(r2[1]), int(r2[2]), 23, 59, 59)
    step = datetime.timedelta(days=1)
    result = []
    while dt < end:
        result.append(dt.strftime('%Y-%m-%d'))
        dt += step
    import datetime as dt
    def convert_date_to_ordinal(date):
        t=dt.datetime.strptime(date,'%Y-%M-%d').date()
        return t.toordinal()

    for z in range(len(result)):
        result[z]=convert_date_to_ordinal(result[z])
    df2=pd.DataFrame(result)
    pre=lm.predict(df2)
    orignal2=df2[0].map(dt.datetime.fromordinal)
    import matplotlib.pyplot as plt
    x1 =orignal2
    y1 =pre
    import matplotlib.pyplot as plt
    from io import StringIO
    import numpy as np
    from django.http import HttpResponse
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    fig = plt.figure(figsize=(9,7))
    plt.plot(x1,y1)
    plt.xlabel('Timeframe')
    plt.ylabel('Waste')
    plt.title('Waste vs Timeframe')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data
def graphh(request):
    return render(request, 'utility/graph.html', {'graph':mlscript()})

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your account has been created! You can now login. ')
            return redirect(r'login')
    else:    
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def home(request):
    wuser = request.user
    waste_list = Waste.objects.filter(tpuser=wuser)
    waste_list_admin = Waste.objects.all()
    tv_list = TransportVehicle.objects.all()
    pp_list = ProcesssingPlant.objects.all()
    lf_list = Landfill.objects.all()
    export(request)
    return render(request,'users/home.html',{'wuser':wuser,'waste_list':waste_list,
    'waste_list_admin':waste_list_admin,'tv_list':tv_list,'pp_list':pp_list,'lf_list':lf_list,}) 

@login_required
def waste_form(request):
    if request.method=='POST':
        waste_form = WasteGenerationForm(request.POST)
        if waste_form.is_valid():
            formm = waste_form.save(commit=False)
            my_p =request.user
            formm.tpuser = my_p
            formm.save()
            messages.success(request,f'Your waste form has been saved. ')

            #saving data to processing plant
            transvehicle = formm.tv
            tv_pp = transvehicle.pp
            pp_temp = ProcesssingPlant.objects.get(pp_id=tv_pp.pp_id)
            pp_temp.total_waste+=formm.quantity
            if(formm.type_waste == 'Non-Recyable'):
                pp_temp.landfill_waste+=formm.quantity
            pp_temp.save()

            #saving data to Landfill
            ll_temp = Landfill.objects.filter(pp=pp_temp)
            if(formm.type_waste == 'Non-Recyable'):
                for ll in ll_temp:
                    if formm.quantity+ll.capacity_filled <= ll.maximum_capacity :
                        ll.capacity_filled+=formm.quantity
                        ll.save()
                        break

            #saving data into WasteML
            if WasteML.objects.filter(date=formm.created_date).count()>0:   #same date has some entry
                waste1=WasteML.objects.get(date=formm.created_date)
                waste1.waste_qty=pp_temp.total_waste
                waste1.save()
            else:
                waste1 = WasteML.objects.create(ppname=pp_temp,date=formm.created_date,waste_qty=pp_temp.total_waste)
                waste1.save()                                               #same date has no entry

            return redirect(r'home')
    else:    
        waste_form = WasteGenerationForm()
    return render(request,'utility/waste_form.html',{'form':waste_form})

@login_required
def tv_form(request):
    if request.method=='POST':
        tv_form = TvGenerationForm(request.POST)
        if tv_form.is_valid():
            tv_form.save()
            messages.success(request,f'You have added a Transport Vehicle.')
            return redirect(r'home')
    else:    
        tv_form = TvGenerationForm()
    return render(request,'utility/tv_form.html',{'form':tv_form})

@login_required
def pp_form(request):
    if request.method=='POST':
        pp_form = PpGenerationForm(request.POST)
        if pp_form.is_valid():
            pp_form.save()
            messages.success(request,f'You have added a Processing plant.')
            return redirect(r'home')
    else:    
        pp_form = PpGenerationForm()
    return render(request,'utility/pp_form.html',{'form':pp_form})
@login_required
def lf_form(request):
    if request.method=='POST':
        lf_form = LfGenerationForm(request.POST)
        if lf_form.is_valid():
            lf_form.save()
            messages.success(request,f'You have added a Landfill.')
            return redirect(r'home')
    else:    
        lf_form = LfGenerationForm()
    return render(request,'utility/lf_form.html',{'form':lf_form})

@login_required
def delete_tv(request, pk):

    template = 'users/home.html'
    TransportVehicle.objects.filter(tv_id=pk).delete()
    return redirect(r'home')
@login_required
def delete_pp(request, pk):

    template = 'users/home.html'
    ProcesssingPlant.objects.filter(pp_id=pk).delete()
    return redirect(r'home')
@login_required
def delete_lf(request, pk):

    template = 'users/home.html'
    Landfill.objects.filter(lf_id=pk).delete()
    return redirect(r'home')

def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(r'home')
    else:
        form = cls(instance=item)
        return render(request, 'utility/edit_item.html', {'form': form})


def update_tv(request, pk):
    return edit_item(request, pk, TransportVehicle, TvUpdateForm)


def update_pp(request, pk):
    return edit_item(request, pk, ProcesssingPlant, PpUpdateForm)


def update_lf(request, pk):
    return edit_item(request, pk, Landfill, LfUpdateForm)

from rest_framework.generics import ListCreateAPIView,GenericAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from .serializers import *

class WasteMLView(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = WasteML.objects.all()
    serializer_class = WasteMLListSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

        
class WasteMLupdateView(RetrieveUpdateDestroyAPIView):
    queryset = WasteML.objects.all()
    serializer_class = WasteMLEditSerializer

