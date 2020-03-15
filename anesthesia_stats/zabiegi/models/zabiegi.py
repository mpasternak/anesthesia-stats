from django.db import models


class Lekarz(models.Model):
    kod = models.IntegerField(primary_key=True)
    imiona = models.TextField()
    nazwisko = models.TextField()


class Pacjent(models.Model):
    mip = models.IntegerField(primary_key=True)
    data_urodzenia = models.DateField()


class Procedura(models.Model):
    kod = models.TextField(primary_key=True)
    nazwa = models.TextField()

    class Meta:
        ordering = ("kod",)


class Jednostka(models.Model):
    kod = models.TextField(primary_key=True)


class Znieczulenie(models.Model):
    nr = models.PositiveIntegerField()

    poczatek = models.DateTimeField()
    koniec = models.DateTimeField(null=True, blank=True)
    czas_trwania = models.IntegerField(null=True, blank=True)

    pacjent = models.ForeignKey(Pacjent, on_delete=models.PROTECT)

    jednostka = models.ForeignKey(Jednostka, on_delete=models.PROTECT)
    lekarze = models.ManyToManyField(Lekarz)
    procedury = models.ManyToManyField(Procedura)
