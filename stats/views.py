from django.shortcuts import render

def stats(request):
	users = User.objects
	return render(request, 'stats/stats.html', {'user':users})
