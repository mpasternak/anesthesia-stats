import datetime

from django.db import IntegrityError
from django.db.models import Min, Max
from django.utils.timezone import make_aware

from zabiegi import models


def integruj_jednostki():
    for w in (
        models.WykazStrona1.objects.all()
        .exclude(dane_operacji_jednostka_wykonująca_kod=None)
        .values_list("dane_operacji_jednostka_wykonująca_kod", flat=True)
        .distinct()
    ):
        models.Jednostka.objects.get_or_create(kod=w)


def integruj_procedury():
    for kod, nazwa in (
        models.WykazStrona1.objects.all()
        .exclude(procedury_medyczne_kod_procedury=None)
        .values_list("procedury_medyczne_kod_procedury", "procedury_medyczne_nazwa")
        .distinct()
    ):
        try:
            models.Procedura.objects.get_or_create(kod=kod, nazwa=nazwa)
        except IntegrityError:
            n = models.Procedura.objects.get(kod=kod)
            raise ValueError(
                f"Procedura juz istnieje {kod}, probowano nazwy {nazwa}, jest {n.nazwa}"
            )


def integruj_lekarzy():
    for (
        personel_uczestniczący_imiona,
        personel_uczestniczący_nazwisko,
        personel_uczestniczący_kod,
    ) in (
        models.WykazStrona1.objects.exclude(personel_uczestniczący_kod=None)
        .values_list(
            "personel_uczestniczący_imiona",
            "personel_uczestniczący_nazwisko",
            "personel_uczestniczący_kod",
        )
        .distinct()
    ):
        models.Lekarz.objects.get_or_create(
            kod=personel_uczestniczący_kod,
            nazwisko=personel_uczestniczący_nazwisko,
            imiona=personel_uczestniczący_imiona,
        )


def integruj_pacjentow():
    for (dane_pacjenta_identyfikator_pacjenta_mip, dane_pacjenta_data_urodzenia,) in (
        models.WykazStrona1.objects.exclude(
            dane_pacjenta_identyfikator_pacjenta_mip=None
        )
        .values_list(
            "dane_pacjenta_identyfikator_pacjenta_mip", "dane_pacjenta_data_urodzenia"
        )
        .distinct()
    ):
        models.Pacjent.objects.get_or_create(
            mip=dane_pacjenta_identyfikator_pacjenta_mip,
            data_urodzenia=dane_pacjenta_data_urodzenia,
        )


def integruj_znieczulenia():
    for w in models.WykazStrona1.objects.exclude(l_p=None):
        poczatek = datetime.datetime.combine(
            w.element_operacji_data_wykonania.date(),
            w.element_operacji_czas_wykonania.time(),
        )
        poczatek = make_aware(poczatek)

        koniec = None
        if w.element_operacji_czas_zakończenia is not None:
            koniec = datetime.datetime.combine(
                w.element_operacji_data_wykonania.date(),
                w.element_operacji_czas_zakończenia.time(),
            )
            koniec = make_aware(koniec)
            if koniec < poczatek:
                koniec += datetime.timedelta(days=1)

        jednostka = models.Jednostka.objects.get(
            kod=w.dane_operacji_jednostka_wykonująca_kod
        )

        pacjent = models.Pacjent.objects.get(
            mip=w.dane_pacjenta_identyfikator_pacjenta_mip
        )

        z, created = models.Znieczulenie.objects.get_or_create(
            nr=w.dane_operacji_księga_nr,
            poczatek=poczatek,
            koniec=koniec,
            czas_trwania=w.element_operacji_czas_trwania_w_minutach,
            jednostka=jednostka,
            pacjent=pacjent,
        )

        lekarz = models.Lekarz.objects.get(kod=w.personel_uczestniczący_kod)
        if lekarz not in z.lekarze.all():
            z.lekarze.add(lekarz)

        procedura = models.Procedura.objects.get(kod=w.procedury_medyczne_kod_procedury)
        if procedura not in z.procedury.all():
            z.procedury.add(procedura)

        z.save()


def pokaz_statystyki():
    z = models.Znieczulenie.objects.all().aggregate(
        min=Min("poczatek"), max=Max("poczatek")
    )
    print(f"Analizowany okres od: {z['min'].date()} do {z['max'].date()}")
    print(f"Liczba znieczuleń ogółem: {models.Znieczulenie.objects.count()}")
    print(f"Znieczulenia wg procedury: ")
    for p in models.Procedura.objects.all():
        print(
            f"{p.nazwa},{models.Znieczulenie.objects.filter(procedury__kod=p.kod).count()}"
        )

    print("Znieczulenia wg jednostek i procedur:")
    print(",".join([p.nazwa for p in models.Procedura.objects.all()]))
    for j in models.Jednostka.objects.all():
        row = []
        for p in models.Procedura.objects.all():
            row.append(
                models.Znieczulenie.objects.filter(jednostka=j, procedury=p).count()
            )
        print(f"{j.kod}," + ",".join([str(x) for x in row]))

    print("Znieczulenia wg miesiąca i jednostki")
    print(",".join(["lip", "sie", "wrz", "paź", "lis", "gru"]))
    for j in models.Jednostka.objects.all():
        row = []
        for miesiac in range(7, 13):
            row.append(
                models.Znieczulenie.objects.filter(
                    jednostka=j, poczatek__month=miesiac
                ).count()
            )
        print(f"{j.kod}," + ",".join([str(x) for x in row]))


def integruj_wszystko():
    integruj_jednostki()
    integruj_procedury()
    integruj_lekarzy()
    integruj_pacjentow()
    integruj_znieczulenia()
