from django.shortcuts import render

# Create your views here.
def main(request):
    render_template = "main.html"
    
    return render(request,render_template)