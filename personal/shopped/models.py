from django.db import models
from time import time
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
import sys, os.path, exifread

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)
    

# Create your models here.

class Photo(models.Model):
    title = models.CharField(max_length=50)
    original = models.ImageField(upload_to=get_upload_file_name)
    transELA = models.ImageField(upload_to='uploaded_files')
    saturated = models.ImageField(upload_to='uploaded_files')
    metaData = models.CharField(max_length = 500)
    
    def __unicode__(self):
        return self.title
       
    def ela(self):
        filename = os.path.realpath('.') + '/static/' + self.original.url
        resaved = filename + '.copy.jpg'
        ela = filename + '.ela.png'
 
        im = Image.open(filename)
 
        im.save(resaved, 'JPEG', quality=95)
        resaved_im = Image.open(resaved)
 
        ela_im = ImageChops.difference(im, resaved_im)
        extrema = ela_im.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0/max_diff
 
        ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
 
        ela_im.save(ela)
        self.transELA = self.original.url + '.ela.png'
        self.save()
        return
        
    def saturate(self):
        filename = os.path.realpath('.') + '/static/' + self.original.url
        saturated = filename + '.saturated.jpg'
        
        im = Image.open(filename)
        converter = ImageEnhance.Color(im)
        im2 = converter.enhance(10.0)
        im2.save(saturated)
        
        self.saturated = self.original.url + '.saturated.jpg'
        self.save()
        return
    
    def exif(self):
        filename = os.path.realpath('.') + '/static/' + self.original.url
        f = open(filename, 'rb')
        
        tags = exifread.process_file(f)
        first = True;
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                if first:
                    first = False;
                    data = self.meta_set.create(key=tag, value=tags[tag], photo=self)
                    data.save()
                else:
                    data = Meta(key=tag, value=tags[tag], photo=self)
                    self.meta_set.add(data)
                    data.save()
                self.save()
        
        return
        
class Meta(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    photo = models.ForeignKey(Photo)
    
    def __unicode__(self):
        return self.key
