import pytest
import os
from xlsx2postgresql.core import XLSXFile

from zabiegi import core


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(__file__), "testdata.xlsx")


@pytest.fixture
def xlsxfile(test_file_path):
    return XLSXFile(test_file_path)


@pytest.fixture
def imported_data(xlsxfile, db):
    from django.db import connection

    cur = connection.cursor()
    for elem in xlsxfile.create_tables():
        cur.execute(elem)
    for elem in xlsxfile.load_data():
        if elem.find("Wykonał: JKOWALSKI") >= 0:
            break
        cur.execute(elem)


@pytest.fixture
def integrated_data(imported_data):
    core.integruj_jednostki()
    core.integruj_procedury()
    core.integruj_pacjentow()
    core.integruj_lekarzy()
    core.integruj_znieczulenia()
