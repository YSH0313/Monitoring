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

    def __str__(self):
        return self.spider_name
