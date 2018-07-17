from django.shortcuts import render
from django.contrib.auth import logout

def home(request):
	return render(request, 'home/home.html')

def logout_view(request):
	logout(request)
	return render(request, 'home/logout.html')
	
def login(request):
	return render(request, 'home/login.html')
