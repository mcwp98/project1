from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from forms import PhotoUpload
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
# Create your views here.
from models import Photo


    
def create(request):
    if request.POST:
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            photo.ela()
            photo.saturate()
            return HttpResponseRedirect('/shopped/analyzed/%d' % photo.id)
            
    else:
        form = PhotoUpload()
            
    args = {}
    args.update(csrf(request))
        
    args['form'] = form
    args['photos'] = Photo.objects.all()
        
    return render_to_response('home.html', args)
    
def analyzed(request, photo_id=1):

    return render_to_response('analyzed.html', {'photo': Photo.objects.get(id=photo_id)})
    

