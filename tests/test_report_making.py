import os
import tempfile
import pytest
from datetime import datetime
from src.reports.report_making import ReportMaking
from src.domain.models import Transaction


@pytest.fixture
def temp_report_dir():
    d = tempfile.mkdtemp()
    yield d
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))


@pytest.fixture
def report_maker(temp_report_dir):
    return ReportMaking(file_path=temp_report_dir)


def test_report_creates_file_when_expenses_present(report_maker, temp_report_dir):
    tx1 = Transaction(type="e", amount=50, category="food",
                      description="", date=datetime(2024, 1, 1))
    tx2 = Transaction(type="i", amount=100, category="salary",
                      description="", date=datetime(2024, 1, 2))

    data = [(1, tx1), (2, tx2)]

    report_maker.print_reports(data)

    assert os.path.exists(os.path.join(temp_report_dir, "report.png"))


def test_report_does_not_create_file_when_no_expenses(report_maker, temp_report_dir):
    tx1 = Transaction(type="i", amount=200, category="salary",
                      description="", date=datetime(2024, 1, 1))

    data = [(1, tx1)]

    report_maker.print_reports(data)

    assert not os.path.exists(os.path.join(temp_report_dir, "report.png"))
