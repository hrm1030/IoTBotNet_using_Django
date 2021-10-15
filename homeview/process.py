from django.shortcuts import render, redirect  
from homeview.forms import LogHistoryForm, UserForm
from homeview.models import LogHistory
from django.contrib import messages  
from django.utils.functional import cached_property
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

