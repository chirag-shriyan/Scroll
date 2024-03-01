from django.shortcuts import render

# Create your views here.

def Search(req):

    DATA = [1,2,3,4,5]

    context = {
        "data": DATA
    }

    return render(req,'search.html',context)
