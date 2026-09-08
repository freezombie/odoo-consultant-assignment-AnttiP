from datetime import date
from decimal import Decimal as D

from hinnoittelu import Customer, Product, Rule, resolve_price


def test_listahinta_kun_ei_saantoja():
    p = Product("TUOLI-01", D("129.00"))
    assert resolve_price(p, Customer("c1"), D("1"), date(2026, 9, 1), []) == D("129.00")


def test_asiakaskohtainen_kiintea_hinta():
    p = Product("POYTA-02", D("890.00"))
    r = Rule(scope="customer", scope_id="c7", product="POYTA-02", min_qty=D("1"),
             valid_from=date(2026, 1, 1), valid_to=date(2026, 12, 31), fixed_price=D("790.00"))
    assert resolve_price(p, Customer("c7"), D("2"), date(2026, 9, 1), [r]) == D("790.00")


def test_ryhma_alennus():
    p = Product("LAMPPU-07", D("50.00"))
    r = Rule(scope="group", scope_id="jalleenmyyjat", product=None, min_qty=D("0"),
             valid_from=date(2026, 1, 1), valid_to=date(2026, 12, 31), discount_pct=D("20"))
    assert resolve_price(p, Customer("c9", ("jalleenmyyjat",)), D("10"), date(2026, 9, 1), [r]) == D("40.00")


def test_cache_is_context_specific():
    p = Product("REG-CACHE-01", D("100.00"))
    r = Rule(scope="customer", scope_id="c1", product="REG-CACHE-01",
             min_qty=D("1"), fixed_price=D("80.00"))
    assert resolve_price(p, Customer("c1"), D("1"), date(2026, 9, 1), [r]) == D("80.00")
    assert resolve_price(p, Customer("c2"), D("1"), date(2026, 9, 1), []) == D("100.00")


def test_customer_scope_beats_group_even_when_group_min_qty_is_higher():
    p = Product("REG-LEVEL-01", D("100.00"))
    customer_rule = Rule(scope="customer", scope_id="c1", product="REG-LEVEL-01",
                          min_qty=D("1"), fixed_price=D("90.00"))
    group_rule = Rule(scope="group", scope_id="g1", product="REG-LEVEL-01",
                      min_qty=D("10"), fixed_price=D("50.00"))
    assert resolve_price(
        p, Customer("c1", ("g1",)), D("10"), date(2026, 9, 1),
        [customer_rule, group_rule],
    ) == D("90.00")


def test_none_valid_from_means_no_lower_bound():
    p = Product("REG-DATE-01", D("100.00"))
    r = Rule(scope="all", product="REG-DATE-01", fixed_price=D("80.00"))
    assert resolve_price(p, Customer("c1"), D("1"), date(2026, 9, 1), [r]) == D("80.00")


def test_valid_to_is_inclusive():
    p = Product("REG-DATE-02", D("100.00"))
    r = Rule(scope="all", product="REG-DATE-02", fixed_price=D("80.00"),
             valid_from=date(2026, 1, 1), valid_to=date(2026, 9, 30))
    assert resolve_price(p, Customer("c1"), D("1"), date(2026, 9, 30), [r]) == D("80.00")


def test_min_qty_is_inclusive():
    p = Product("REG-QTY-01", D("100.00"))
    r = Rule(scope="all", product="REG-QTY-01", min_qty=D("10"), fixed_price=D("80.00"))
    assert resolve_price(p, Customer("c1"), D("10"), date(2026, 9, 1), [r]) == D("80.00")


def test_rounding_is_half_up():
    p = Product("REG-ROUND-01", D("2.675"))
    assert resolve_price(p, Customer("c1"), D("1"), date(2026, 9, 1), []) == D("2.68")
