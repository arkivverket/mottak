import pytest
from models import AVScanResult


@pytest.fixture
def _scan_result() -> AVScanResult:
    clean = 10
    virus = 0
    skipped = 0
    return AVScanResult(clean, virus, skipped)


def test_avscanresult_init(_scan_result):
    result = AVScanResult(10, 0, 0)
    assert result == _scan_result


def test_status_has_correct_values():
    scan_found_virus = AVScanResult(9, 1, 0)
    scan_found_nothing = AVScanResult(10, 0, 0)
    assert scan_found_virus.status == "Ikke ok"
    assert scan_found_nothing.status == "ok"


def test_correct_message_when_no_virus_found(_scan_result):
    expected_message = (
        "Status etter virus scan: ok\n\n"
        "Antall filer kontrollert: 10\n"
        "    - Filer uten virus: 10\n"
        "    - Filer med virus: 0\n"
        "Antall filer ikke kontrollert pga. filstørrelse: 0"
    )

    assert expected_message == _scan_result.get_message()
    # assert _scan_result.get_message() == expected_message


def test_correct_message_when_virus_found(_scan_result):
    expected_message = (
        "Status etter virus scan: Ikke ok\n\n"
        "Antall filer kontrollert: 10\n"
        "    - Filer uten virus: 8\n"
        "    - Filer med virus: 2\n"
        "Antall filer ikke kontrollert pga. filstørrelse: 0"
    )
    actual = AVScanResult(8, 2, 0)
    assert expected_message == actual.get_message()
