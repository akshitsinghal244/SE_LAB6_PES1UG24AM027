import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# ---------- Example tests (from starter file) ----------
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_clean_record():
    assert license_action(2, False, False) == "none"

# ================= speeding_fine =================
# speed <= limit: True / False
def test_speed_equal_to_limit():             # boundary: <= is True
    assert speeding_fine(60, 60, "city") == 0

def test_speed_just_over_limit():            # <= is False
    assert speeding_fine(61, 60, "city") == 500

# zone: school / highway / else
def test_school_zone_base():
    assert speeding_fine(70, 60, "school") == 2000

def test_highway_zone_base():
    assert speeding_fine(70, 60, "highway") == 1000

def test_city_zone_base():
    assert speeding_fine(70, 60, "city") == 500

def test_unknown_zone_uses_default():
    assert speeding_fine(70, 60, "rural") == 500

# excess: > 40 / > 20 / otherwise (plus boundaries)
def test_excess_over_40_triple():
    assert speeding_fine(101, 60, "city") == 1500      # excess 41

def test_excess_exactly_40_double():
    assert speeding_fine(100, 60, "city") == 1000      # excess 40, not > 40

def test_excess_over_20_double():
    assert speeding_fine(81, 60, "city") == 1000       # excess 21

def test_excess_exactly_20_single():
    assert speeding_fine(80, 60, "city") == 500        # excess 20, not > 20

# ================= license_action =================
# points >= 12
def test_12_points_commercial_revoke():
    assert license_action(12, True, False) == "revoke"

def test_12_points_private_suspend():
    assert license_action(12, False, False) == "suspend"

# points >= 8 (8..11)
def test_8_points_repeat_suspend():
    assert license_action(8, False, True) == "suspend"

def test_8_points_first_offence_warning():
    assert license_action(8, False, False) == "warning"

def test_11_points_is_not_12():              # boundary below 12
    assert license_action(11, True, False) == "warning"

# points >= 4 (4..7)
def test_4_points_notice():
    assert license_action(4, False, False) == "notice"

def test_7_points_is_not_8():                # boundary below 8
    assert license_action(7, False, True) == "notice"

# points < 4
def test_3_points_none():                    # boundary below 4
    assert license_action(3, False, False) == "none"

# ================= total_penalty =================
def test_empty_list():                       # loop body never runs
    assert total_penalty([]) == 0

def test_normal_total_under_cap():            # total > 10000 is False
    assert total_penalty([500, 1500]) == 2000

def test_total_exactly_at_cap():              # boundary: 10000 not > 10000
    assert total_penalty([10000]) == 10000

def test_total_over_cap_is_limited():         # total > 10000 is True
    assert total_penalty([6000, 6000]) == 10000

def test_negative_fine_raises():              # fine < 0 True
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -5])

def test_zero_fine_allowed():                 # boundary: 0 is not < 0
    assert total_penalty([0, 100]) == 100
