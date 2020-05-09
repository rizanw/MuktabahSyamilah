from django.shortcuts import render , redirect 
from .services import getResult
import time

def index(request):
    return render(request, 'main/index.html', {})

def result(request):
    search = request.GET.get('search')
    if search:
        start_time = time.time()
        res = getResult(search)
        print(res)
        len_result = len(res)
        total_time = (time.time() - start_time)
        return render(request, 'main/result.html', {"results": res, "query": search, "totalTime": total_time, "lenResult": len_result})
    else:
        return redirect('/')                              