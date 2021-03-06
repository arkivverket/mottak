import pytest
from app.models import AVScanResult


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
    assert scan_found_virus.get_status() == "Ikke ok"
    assert scan_found_nothing.get_status() == "ok"


def test_correct_message_when_no_virus_found(_scan_result):
    expected_message = (
        "Status etter virus scan: ok\n\n"
        "Antall filer kontrollert: 10 av 10\n"
        "    - Filer uten virus: 10\n"
        "    - Filer med virus: 0\n"
        "    - Filer ikke kontrollert pga. filstørrelse: 0"
    )

    assert expected_message == _scan_result.generate_message()
    # assert _scan_result.get_message() == expected_message


def test_correct_message_when_virus_found():
    expected_message = (
        "Status etter virus scan: Ikke ok\n\n"
        "Antall filer kontrollert: 10 av 10\n"
        "    - Filer uten virus: 8\n"
        "    - Filer med virus: 2\n"
        "    - Filer ikke kontrollert pga. filstørrelse: 0"
    )
    actual = AVScanResult(8, 2, 0)
    assert expected_message == actual.generate_message()


def test_correct_message_when_skipped_files():
    expected_message = (
        "Status etter virus scan: Ikke ok\n\n"
        "Antall filer kontrollert: 10 av 15\n"
        "    - Filer uten virus: 8\n"
        "    - Filer med virus: 2\n"
        "    - Filer ikke kontrollert pga. filstørrelse: 5"
    )
    actual = AVScanResult(8, 2, 5)
    assert expected_message == actual.generate_message()
