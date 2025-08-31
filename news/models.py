from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField



class News(models.Model):
    news_title = models.CharField(max_length=100)
    news_desc = HTMLField()
    news_img = models.FileField(upload_to='news_img',max_length=300,null=True,default=None)
    news_slug =  AutoSlugField(populate_from="news_title",unique=True,null=True,blank=None)
    
