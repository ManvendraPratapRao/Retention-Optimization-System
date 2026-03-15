import pytest
from app.decision_engine import (
    calculate_base_remaining_value,
    calculate_expected_gain,
    make_decision
)
from app.config import BusinessConfig

@pytest.fixture
def business_config():
    return BusinessConfig(
        avg_lifetime=36,
        floor_months=6,
        margin_pct=0.5,
        retention_success_rate=0.2,
        contact_cost=5.0,
        incentive_cost=20.0
    )

def test_calculate_base_remaining_value_normal(business_config):
    # tenure 12, monthly 100 -> rem months = 36-12=24. margin = 100*0.5=50. BRV = 24*50 = 1200
    brv, margin = calculate_base_remaining_value(12, 100, business_config)
    assert brv == 1200.0
    assert margin == 50.0

def test_calculate_base_remaining_value_floor(business_config):
    # tenure 35, monthly 100 -> rem months = max(36-35, 6) = 6. margin 50. BRV = 6*50 = 300
    brv, margin = calculate_base_remaining_value(35, 100, business_config)
    assert brv == 300.0

def test_calculate_expected_gain_positive(business_config):
    # BRV 1000, p_churn 0.8, success 0.2, cost 25
    # recovery = 1000 * 0.8 * 0.2 = 160
    # gain = 160 - 25 = 135
    gain, roi, cost = calculate_expected_gain(0.8, 1000, business_config)
    assert gain == 135.0
    assert cost == 25.0
    assert roi == 135.0 / 25.0

def test_calculate_expected_gain_negative(business_config):
    # BRV 100, p_churn 0.1, success 0.2, cost 25
    # recovery = 100 * 0.1 * 0.2 = 2
    # gain = 2 - 25 = -23
    gain, roi, cost = calculate_expected_gain(0.1, 100, business_config)
    assert gain == -23.0
    assert roi < 0

def test_make_decision():
    assert make_decision(10.0) == "Retain"
    assert make_decision(-5.0) == "Let Go"
    assert make_decision(0.0) == "Let Go" # Threshold check
