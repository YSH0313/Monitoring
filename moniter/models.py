from django.db import models


# Create your models here.
class registered(models.Model):
    table_name = models.CharField(max_length=255)
    table_dimensions = models.CharField(max_length=255)

class user(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class data_count(models.Model):
    count = models.IntegerField(default=0, null=True)
    dimensions = models.CharField(max_length=255, null=True)
    time_date = models.CharField(max_length=30, null=True)

class month_datacount(models.Model):
    count = models.IntegerField(default=0, null=True)
    dimensions = models.CharField(max_length=255, null=True)
    time_date = models.CharField(max_length=30, null=True)

class important_source(models.Model):
    source_name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    dimensions = models.CharField(max_length=255, null=True)
    yesterday_num = models.CharField(max_length=255, null=True)
    today_num = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=255, null=True)


class spider_lists(models.Model):
    spider_name = models.CharField(max_length=255, null=True)
    interval_time = models.CharField(max_length=255, null=True)
    data_base = models.CharField(max_length=255, null=True)
    start_time = models.CharField(max_length=255, null=True)
    end_time = models.CharField(max_length=255, null=True)
    status = models.IntegerField(null=True)
    server = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.spider_name

class creat_project_lists(models.Model):
    project_name = models.CharField(max_length=255, null=True)
    contrller = models.CharField(max_length=255, null=True)
    spider_count = models.CharField(max_length=255, null=True)
    project_desc = models.CharField(max_length=255, null=True)
    created_time = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=10, null=True)

    def __str__(self):
        return  self.project_name

class creat_spider_lists(models.Model):
    projectname = models.CharField(max_length=255, null=True)
    spidername = models.CharField(max_length=255, null=True)
    islong = models.CharField(max_length=255, null=True)
    spiderdesc = models.CharField(max_length=255, null=True)
    creattime = models.CharField(max_length=255, null=True)
    lasttime = models.CharField(max_length=255, null=True)
    laststatus = models.CharField(max_length=255, null=True)
    remarks = models.CharField(max_length=255, null=True)
    node = models.CharField(max_length=255, null=True)
    param = models.CharField(max_length=255, null=True)
    count = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername

class spider_prarm(models.Model):
    spidername = models.CharField(max_length=255, null=True)
    varname = models.CharField(max_length=255, null=True)
    vartype = models.CharField(max_length=255, null=True)
    varvalue = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername

class spider_start(models.Model):
    spidername = models.CharField(max_length=255, null=True)
    startrequest = models.CharField(max_length=255, null=True)
    headers = models.TextField(blank=True)
    requesttype = models.CharField(max_length=255, null=True)
    formdata = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername

class page_set(models.Model):
    spidername = models.CharField(max_length=255, null=True)
    pageurl = models.CharField(max_length=255, null=True)
    pagecount = models.CharField(max_length=255, null=True)
    pagevar = models.CharField(max_length=255, null=True)
    callname = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername

class lists_set(models.Model):
    spidername = models.CharField(max_length=255, null=True)
    listsxpath = models.CharField(max_length=255, null=True)
    contentxpath = models.CharField(max_length=255, null=True)
    callname = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername

class content_set(models.Model):
    spidername = models.CharField(max_length=255, null=True)
    fieldname = models.CharField(max_length=255, null=True)
    rule = models.CharField(max_length=255, null=True)
    is_many = models.CharField(max_length=255, null=True)
    notename = models.CharField(max_length=255, null=True)

    def __str__(self):
        return  self.spidername