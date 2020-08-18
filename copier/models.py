from django.db import models

# Create your models here.


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    scanner = models.FileField()

    def __str__(self):
        return self.name


class DriverFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(default=None, unique=True)

    def __str__(self):
        return self.file.name


class Copier(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='copiers')
    color_mono = models.IntegerField(default=0)
    bit = models.IntegerField(default=0)
    model_name = models.CharField(max_length=150, unique=True)
    driver_file = models.ForeignKey(DriverFile, on_delete=models.CASCADE, related_name='copiers')

    def __str__(self):
        return "{}-{}".format(self.company, self.model_name)
