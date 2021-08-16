from django.db import models

# Create your models here.

'''class Station(models.Model):
    station_name_hira = models.CharField(max_length=100)
    station_name_kanji = models.CharField(max_length=100)
    station_name_kata = models.CharField(max_length=100)
    first_letter = models.CharField(max_length=1)
    last_letter = models.CharField(max_length=1)
    isends_n = models.BooleanField
    prf_no = models.IntegerField
    city_name = models.CharField(max_length=100)
    jr_co_name = models.CharField(max_length=100)
    rail_name = models.CharField(max_length=200)

    def __str__(self):
        return self.station_name_kanji
        '''

class Prefecture(models.Model):
    prf_no = models.IntegerField(default=0)
    prf_name = models.CharField(max_length=10)

    def __str__(self):
        return self.prf_name