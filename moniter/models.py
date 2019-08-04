from django.db import models


# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class data_count(models.Model):
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    database_name = models.CharField(max_length=255)



class app_num(models.Model):
    rank = models.CharField(max_length=255, null=True)
    appname = models.CharField(max_length=255, null=True)
    applogo = models.CharField(max_length=255, null=True)
    fclassname = models.CharField(max_length=255, null=True)
    kclassname = models.CharField(max_length=255, null=True)
    usenum = models.CharField(max_length=255, null=True)
    growth = models.CharField(max_length=255, null=True)
    daymachinenum = models.CharField(max_length=255, null=True)
    dmgrowth = models.CharField(max_length=255, null=True)
    usetime = models.CharField(max_length=255, null=True)
    timegrowth = models.CharField(max_length=255, null=True)
    timename = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.appname


class spider_lists(models.Model):
    spider_name = models.CharField(max_length=255, null=True)
    interval_time = models.CharField(max_length=255, null=True)
    data_base = models.CharField(max_length=255, null=True)
    start_time = models.CharField(max_length=255, null=True)
    end_time = models.CharField(max_length=255, null=True)
    status = models.IntegerField(null=True)
    server = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.spider_name
