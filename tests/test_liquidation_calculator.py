import pytest

from hyperliquid_liquidation.liquidation_calculator import (
    LiquidationCalculator,
    create_sample_positions,
)


@pytest.fixture
def calc():
    return LiquidationCalculator()


def test_isolated_long_matches_formula(calc):
    # BTC max leverage 50x -> maintenance rate 0.5 / 50 = 1 %
    liq = calc.calculate_position_liquidation(
        entry_price=95_000, size=1.0, leverage=10, margin_type="isolated", coin="BTC"
    )
    assert liq == pytest.approx(95_000 * (1 - 1 / 10 + 0.01))


def test_isolated_short_matches_formula(calc):
    liq = calc.calculate_position_liquidation(
        entry_price=95_000, size=-1.0, leverage=10, margin_type="isolated", coin="BTC"
    )
    assert liq == pytest.approx(95_000 * (1 + 1 / 10 - 0.01))


@pytest.mark.parametrize("margin_type", ["isolated", "cross"])
@pytest.mark.parametrize("leverage", [2, 5, 20, 50])
def test_liquidation_is_on_the_losing_side(calc, margin_type, leverage):
    long_liq = calc.calculate_position_liquidation(3_500, 2.0, leverage, margin_type, "ETH")
    short_liq = calc.calculate_position_liquidation(3_500, -2.0, leverage, margin_type, "ETH")
    assert 0 < long_liq < 3_500 < short_liq


def test_zero_size_has_no_liquidation_price(calc):
    assert calc.calculate_position_liquidation(95_000, 0, 10, "isolated", "BTC") is None


def test_aggregate_positions_bins_sample_book(calc):
    positions = create_sample_positions("BTC", 95_000, count=300)
    data = calc.aggregate_positions(positions, "BTC", 95_000)

    assert data.coin == "BTC"
    assert data.current_price == 95_000
    n = len(data.price_levels)
    assert n > 0
    assert len(data.long_values) == len(data.short_values) == n
    assert (data.long_values >= 0).all() and (data.short_values >= 0).all()
    assert data.long_values.sum() + data.short_values.sum() > 0
