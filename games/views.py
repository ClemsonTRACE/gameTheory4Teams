from django.shortcuts import render

# Create your views here.
def bos(request):
	return render(request, "bos.html")

def centipede(request):
	return render(request, "centipede.html")

def hawkdove(request):
	return render(request, "hawk-dove.html")

def pd(request):
	return render(request, "pd.html")

def ultimatum(request):
	return render(request, "ultimatum.html")