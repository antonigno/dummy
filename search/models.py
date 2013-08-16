from django.db import models

class Meta(models.Model):
    keyword = models.CharField(max_length=500)
    rank = models.IntegerField(default=1)
    def __unicode__(self):
        return "%s(rank:%d)" %(self.keyword, self.rank)

class WebSite(models.Model):
    url = models.URLField()
    pub_date = models.DateTimeField('last modified')
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)
    meta = models.ManyToManyField(Meta)
    def __unicode__(self):
        return self.title



