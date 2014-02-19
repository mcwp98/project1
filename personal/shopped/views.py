from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from forms import PhotoUpload
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
# Create your views here.
from models import Photo, Meta


    
def create(request):
    if request.POST:
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            photo.ela()
            photo.saturate()
            photo.exif()
            return HttpResponseRedirect('/shopped/analyzed/%d' % photo.id)
            
    else:
        form = PhotoUpload()
            
    args = {}
    args.update(csrf(request))
        
    args['form'] = form
    args['photos'] = Photo.objects.all()
        
    return render_to_response('home.html', args)
    
def analyzed(request, photo_id=1):
    photo = Photo.objects.get(id=photo_id)
    photo.meta_set.select_related()
    
    args = {}
    args['photo'] = photo
    args['metas'] = photo.meta_set.select_related()
    
    temp_id = int(photo_id)
    
    try:
        last = Photo.objects.get(id=(temp_id-1)).id
    except Photo.DoesNotExist:
        last = None
    args['last'] = last
    
    try:
        next = Photo.objects.get(id=(temp_id+1)).id
    except Photo.DoesNotExist:
        next = None
    args['next'] = next
        
    return render_to_response('analyzed.html', args)
    

