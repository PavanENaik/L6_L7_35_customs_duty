
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# Duty rate tests
def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_electronics_fta_rate():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta_rate():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta_rate():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta_rate():
    assert duty_rate("clothing", "US") == 0.12


def test_other_category_rate():
    assert duty_rate("toys", "US") == 0.15


def test_prohibited_weapons():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("weapons", "FTA")


def test_prohibited_narcotics():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("narcotics", "FTA")


# Total duty tests
def test_negative_value():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -100, "FTA", False)


def test_gift_below_exemption():
    assert total_duty("electronics", 4000, "FTA", True) == 0


def test_gift_at_exemption():
    assert total_duty("electronics", 5000, "FTA", True) == 0


def test_gift_above_exemption():
    assert total_duty("electronics", 6000, "FTA", True) == 100


def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_non_gift_at_low_value_limit():
    assert total_duty("electronics", 1000, "FTA", False) == 0


def test_minimum_duty_applied():
    assert total_duty("clothing", 5100, "FTA", True) == 50


def test_normal_duty_calculation():
    assert total_duty("electronics", 2000, "FTA", False) == 200


# Clearance channel tests
def test_prohibited_item_refused():
    assert clearance_channel(100, "weapons", True) == "refuse"


def test_high_value_inspection():
    assert clearance_channel(100001, "books", True) == "inspect"


def test_missing_documents_inspection():
    assert clearance_channel(25000, "books", False) == "inspect"


def test_green_clearance():
    assert clearance_channel(10000, "books", True) == "green"
