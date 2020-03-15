from zabiegi import core, models
import pytest


def test_integruj_jednostki(imported_data):
    core.integruj_jednostki()
    assert models.Jednostka.objects.all().count() == 1


def test_integruj_procedury(imported_data):
    core.integruj_procedury()
    assert models.Procedura.objects.count() == 1


def test_integruj_lekarzy(imported_data):
    core.integruj_lekarzy()
    assert models.Lekarz.objects.count() == 4


def test_integruj_pacjentow(imported_data):
    core.integruj_pacjentow()
    assert models.Pacjent.objects.count() == 5


def test_integruj_znieczulenia(imported_data):
    core.integruj_jednostki()
    core.integruj_procedury()
    core.integruj_pacjentow()
    core.integruj_lekarzy()

    core.integruj_znieczulenia()
    assert models.Znieczulenie.objects.count() == 5

    zn = models.Znieczulenie.objects.get(nr=313)
    assert zn.lekarze.count() == 2
    assert zn.procedury.count() == 1


def test_pokaz_statystyki(integrated_data):
    core.pokaz_statystyki()


def test_integruj_wszystko(imported_data):
    core.integruj_wszystko()
