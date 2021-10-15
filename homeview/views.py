from django.shortcuts import render, redirect  
from homeview.forms import LogHistoryForm, UserForm
from homeview.models import LogHistory
from django.contrib import messages  
from django.utils.functional import cached_property
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage
import sys
import Phase1.phaseOneProcessor as phaseOne
import Phase2.phaseTwoProcessor as phaseTwo
import os
from django.http import HttpResponse
import json
from datetime import datetime

def create_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    email = request.GET.get('email')
    user = User.objects.create_user('SystemAdmin', 'SystemAdmin@gmail.com', 'root')
    user.is_staff = '2'
    user.save()
def emp(request):  
    if request.method == "POST":  
        form = LogHistoryForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = LogHistoryForm()  
    return render(request,'index.html',{'form':form}) 

def login(request):
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        return render(request, 'login.html')
def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request)
        request.session['username'] = username
        request.session['role'] = user.is_staff
        request.session['email'] = user.email
        if request.session['role'] == 1 or request.session['role'] == 2:
            return redirect('/main')
        if request.session['role'] == 3:
            return redirect('/log_history')
        else:
            messages.success(request, 'Your account is not yet activated.')
            return redirect('/')

    else:
        messages.success(request, 'Please enter your username and password exactly.')
        return redirect('/')
def signout(request):
    logout(request)
    return redirect('/')
def main(request):
    if request.session['role'] == 1 or request.session['role'] == 2:
        return render(request, 'main.html')
    else:
        return redirect('/log_history')
def file_upload(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    return HttpResponse({uploaded_file_url : uploaded_file_url})
def log_history(request):
    if request.session['role'] == 1 or request.session['role'] == 3:
        loghistoryAll = LogHistory.objects.all()  
        return render(request, 'log_history.html', {'loghistoryAll':loghistoryAll})
    else:
        return redirect('/main')
def show(request):  
    loghistoryAll = LogHistory.objects.all()  
    return render(request,"show.html",{'loghistoryAll':loghistoryAll})  
def edit(request, id):  
    logbyid = LogHistory.objects.get(id=id)  
    return render(request,'edit.html', {'logbyid':logbyid})  
def update(request, id):  
    logbyid = LogHistory.objects.get(id=id)  
    form = LogHistoryForm(request.POST, instance = logbyid)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'logbyid': logbyid})  
def destroy(request, id):  
    logbyid = LogHistory.objects.get(id=id)  
    logbyid.delete()  
    return redirect("/show")  
# trainmodel
def trainmodel(request):
    strReturnMsg,strStatusMsg = phaseOne.beginTrain()
    responseData = {
        
        'message': strReturnMsg,
        'status':strStatusMsg
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")
# clear the trainmodel
def clearmodel(request):
    strReturnMsg = "Success"
    for idx in range(8):
        Pkl_Filename = f'ml_model/Pickle_RL_Model{idx+1}.pkl' 
        os.remove(Pkl_Filename)

    responseData = {
        
        'message': strReturnMsg
        
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")  

# Create your tests here.
def detector(request):  
    pcappath = request.POST['path']
    pcappath = pcappath.split("\\")[-1]
    strReturnMsg, stateValue = phaseTwo.beginTestforAttack(pcappath)
    
    strtoday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    if(stateValue == 0 or stateValue == -1):
        strResult = ""
        if(stateValue == 0):
            strResult = "Normal"
        if(stateValue == -1):
            strResult = "Abnormal"
        #    strResult,pcappath,strtoday
        logsave = LogHistory()
        logsave.logid = 7
        logsave.logdate = strtoday
        logsave.logname = pcappath
        logsave.logstate = strResult
        logsave.save()
    responseData = {
        
        'message': strReturnMsg,
        'state' : stateValue
    }

    return HttpResponse(json.dumps(responseData), content_type="application/json")  

def getmessage1(request):
    path = "./homeview/static/message/phase1_output.ms"
    message_file = open(path, "r")
    data = message_file.read()
    responseData = {
        
        'message': data,
        'state' : "success"
    }

    return HttpResponse(json.dumps(responseData), content_type="application/json")
    
def getmessage2(request):
    path = "./homeview/static/message/phase2_output.ms"
    message_file = open(path, "r")
    data = message_file.read()
    responseData = {
        
        'message': data,
        'state' : "success"
    }

    return HttpResponse(json.dumps(responseData), content_type="application/json")