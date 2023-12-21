from django.db import models

# Create your models here.
class Aktyor(models.Model):
    ism = models.CharField(max_length=30)
    davlat = models.CharField(max_length=30)
    jins = models.CharField(max_length=10 ,blank=True)
    tugilgan_yil = models.DateField(max_length=10)

    def __str__(self):
        return self.ism

class Kino(models.Model):
    nom = models.CharField(max_length=30)
    janr = models.CharField(max_length=30)
    yil = models.DateField(blank=True)
    aktyorlar = models.ManyToManyField(Aktyor)

    def __str__(self) -> str:
        return self.nom
    
class Tarif(models.Model):
    nom = models.CharField(max_length=30)
    narx = models.PositiveBigIntegerField()
    davomiylik = models.CharField(max_length=60)

    def __str__(self):
        return self.nom
    
class Izoh(models.Model):
    matn = models.TextField()
    # user = mode
    sana = models.DateField()
    kino = models.ForeignKey(Kino, on_delete=models.CASCADE)
    baho = models.PositiveSmallIntegerField()