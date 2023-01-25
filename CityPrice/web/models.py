# Create your models here.
from django.db import models


class District(models.Model):
    """ District model """
    no = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    population = models.FloatField()
    area = models.FloatField()

    def __str__(self):
        return self.name


class Neighbourhood(models.Model):
    """ Neighbourhood model """
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=30)
    # foreign key & delete the recode if the district is deleted
    # district = models.ForeignKey(to=District, to_field='no', on_delete=models.CASCADE)
    # set null if the district is deleted
    # district = models.ForeignKey(to=District, to_field='no', on_delete=models.SET_NULL, null=True)
    price = models.FloatField()


class Location(models.Model):
    """ Location model """
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Park(models.Model):
    """ Park model """
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # district = models.CharField(max_length=30)
    district = models.ForeignKey(to=District, to_field='no', on_delete=models.CASCADE)
    area = models.FloatField()


class Hospital(models.Model):
    """ Hospital model """
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=30)

    hospitalLevelChoices = (
        (1, '无等级'),
        (2, '一乙'),
        (3, '一甲'),
        (4, '二乙'),
        (5, '二甲'),
        (6, '三乙'),
        (7, '三甲')
    )
    level = models.SmallIntegerField(choices=hospitalLevelChoices)  # hospital level


class School(models.Model):
    """ School model """
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=30)

    schoolLevelChoices = (
        (1, '幼儿园'),
        (2, '小学'),
        (3, '初中'),
        (4, '职业高中'),
        (5, '普通高中')
    )
    level = models.SmallIntegerField(choices=schoolLevelChoices)  # school type
