from services import market


def test_known_set_returns_hardcoded_price():
    assert market.get_market_price("10329") == 54.99
    assert market.get_market_price("10311") == 52.00
    assert market.get_market_price("10309") == 58.50


def test_unknown_set_returns_price_in_expected_growth_range():
    price = market.get_market_price("99999-does-not-exist")
    assert 49.99 * 1.05 <= price <= 49.99 * 1.15
