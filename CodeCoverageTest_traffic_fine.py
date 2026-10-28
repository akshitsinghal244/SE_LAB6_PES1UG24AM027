import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# ---------- Example tests (from starter file) ----------
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_clean_record():
    assert license_action(2, False, False) == "none"

# ---------- speeding_fine: execute every line ----------
def test_school_zone_excess_over_40():
    # excess = 50 -> base 2000 * 3
    assert speeding_fine(100, 50, "school") == 6000

def test_highway_zone_excess_over_20():
    # excess = 30 -> base 1000 * 2
    assert speeding_fine(130, 100, "highway") == 2000

def test_city_zone_small_excess():
    # excess = 10 -> base 500 (no multiplier)
    assert speeding_fine(70, 60, "city") == 500

# ---------- license_action: execute every return line ----------
def test_revoke_commercial():
    assert license_action(12, True, False) == "revoke"

def test_suspend_private_12_points():
    assert license_action(12, False, False) == "suspend"

def test_suspend_repeat_offender():
    assert license_action(8, False, True) == "suspend"

def test_warning_first_offence():
    assert license_action(8, False, False) == "warning"

def test_notice():
    assert license_action(5, False, False) == "notice"

# ---------- total_penalty: execute raise and cap lines ----------
def test_negative_fine_raises():
    with pytest.raises(ValueError):
        total_penalty([100, -5])

def test_total_is_capped():
    assert total_penalty([6000, 6000]) == 10000
