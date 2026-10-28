
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# Branch tests for duty_rate()
def test_duty_rate_prohibited_and_allowed():
    with pytest.raises(ValueError):
        duty_rate("weapons", "FTA")

    with pytest.raises(ValueError):
        duty_rate("narcotics", "FTA")

    assert duty_rate("electronics", "FTA") == 0.10
    assert duty_rate("electronics", "US") == 0.20

    assert duty_rate("clothing", "FTA") == 0.05
    assert duty_rate("clothing", "US") == 0.12

    assert duty_rate("books", "US") == 0
    assert duty_rate("toys", "US") == 0.15


# Branch tests for total_duty()
def test_total_duty_negative_and_nonnegative():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -1, "FTA", False)

    assert total_duty("electronics", 2000, "FTA", False) == 200


def test_gift_exemption_branches():
    assert total_duty("electronics", 4000, "FTA", True) == 0
    assert total_duty("electronics", 5000, "FTA", True) == 0
    assert total_duty("electronics", 6000, "FTA", True) == 100


def test_non_gift_value_branches():
    assert total_duty("electronics", 1000, "FTA", False) == 0
    assert total_duty("electronics", 1001, "FTA", False) == pytest.approx(100.1)


def test_minimum_duty_branches():
    # Positive duty below 50: minimum duty applies
    assert total_duty("clothing", 5100, "FTA", True) == 50

    # Zero duty: minimum duty does not apply
    assert total_duty("books", 2000, "US", False) == 0

    # Duty above 50: minimum duty does not apply
    assert total_duty("electronics", 2000, "FTA", False) == 200


# Branch tests for clearance_channel()
def test_prohibited_and_allowed_clearance():
    assert clearance_channel(100, "weapons", True) == "refuse"
    assert clearance_channel(100, "narcotics", False) == "refuse"

    assert clearance_channel(100001, "books", True) == "inspect"


def test_value_and_document_branches():
    # Value at the high-value threshold
    assert clearance_channel(100000, "books", True) == "green"

    # Above 20000 with and without documents
    assert clearance_channel(25000, "books", False) == "inspect"
    assert clearance_channel(25000, "books", True) == "green"

    # At 20000 and ordinary low-value item
    assert clearance_channel(20000, "books", False) == "green"
    assert clearance_channel(10000, "books", True) == "green"
