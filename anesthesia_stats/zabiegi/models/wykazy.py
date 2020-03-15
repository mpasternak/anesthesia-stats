from django.db import models


class WykazStrona1(models.Model):
    l_p = models.DecimalField(max_digits=65535, decimal_places=65535, primary_key=True)
    dane_operacji_jednostka_wykonująca_kod = models.TextField(blank=True, null=True)
    element_operacji_data_wykonania = models.DateTimeField(blank=True, null=True)
    element_operacji_czas_wykonania = models.DateTimeField(blank=True, null=True)
    element_operacji_czas_zakończenia = models.DateTimeField(blank=True, null=True)
    dane_operacji_księga_nr = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    element_operacji_czas_wykonania2 = models.DateTimeField(blank=True, null=True)
    element_operacji_czas_zakończenia3 = models.DateTimeField(blank=True, null=True)
    element_operacji_czas_trwania_w_minutach = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    personel_uczestniczący_imiona = models.TextField(blank=True, null=True)
    personel_uczestniczący_nazwisko = models.TextField(blank=True, null=True)
    jednostka_zlecająca_nazwa = models.TextField(blank=True, null=True)
    personel_uczestniczący_kod = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    personel_uczestniczący_rola_kod = models.TextField(blank=True, null=True)
    element_operacji_typ_elementu_leczenia = models.TextField(blank=True, null=True)
    dane_pacjenta_identyfikator_pacjenta_mip = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    dane_pacjenta_data_urodzenia = models.DateTimeField(blank=True, null=True)
    procedury_medyczne_kod_procedury = models.TextField(blank=True, null=True)
    procedury_medyczne_nazwa = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "wykaz_strona_1"
