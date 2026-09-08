"""Hinnoittelusääntöjen ratkaisu — toteuttaa SPEC.md:n.

Toteutettu AI-koodausagentilla määrittelyn pohjalta. Testit (test_hinnoittelu.py) vihreänä.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


@dataclass(frozen=True)
class Product:
    sku: str
    list_price: Decimal


@dataclass(frozen=True)
class Customer:
    id: str
    group_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class Rule:
    scope: str                          # "customer" | "group" | "all"
    scope_id: Optional[str] = None      # asiakas-id tai ryhmä-id; None kun scope == "all"
    product: Optional[str] = None       # sku tai None = kaikki tuotteet
    min_qty: Decimal = Decimal("0")
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    fixed_price: Optional[Decimal] = None
    discount_pct: Optional[Decimal] = None


_LEVEL = {"customer": 2, "group": 1, "all": 0}

# Hintakyselyjä tulee paljon (SPEC kohta 8) — välimuisti säästää turhan uudelleenlaskennan.
_cache: dict[tuple[Product, Customer, Decimal, date, tuple[Rule, ...]], Decimal] = {}


def _applies(rule: Rule, product: Product, customer: Customer, qty: Decimal, on: date) -> bool:
    if rule.product is not None and rule.product != product.sku:
        return False
    if rule.scope == "customer" and rule.scope_id != customer.id:
        return False
    if rule.scope == "group" and rule.scope_id not in customer.group_ids:
        return False
    if qty < rule.min_qty:
        return False
    if rule.valid_from is not None and rule.valid_from > on:
        return False
    if rule.valid_to is not None and on > rule.valid_to:
        return False
    return True


def _rule_price(rule: Rule, product: Product) -> Decimal:
    if rule.fixed_price is not None:
        return rule.fixed_price
    if rule.discount_pct is None:
        raise ValueError("Rule must define fixed_price or discount_pct")
    return product.list_price * (Decimal(1) - rule.discount_pct / Decimal(100))


def resolve_price(product: Product, customer: Customer, qty: Decimal, on: date, rules: list[Rule]) -> Decimal:
    cache_key = (product, customer, qty, on, tuple(rules))
    if cache_key in _cache:
        return _cache[cache_key]

    matching = [r for r in rules if _applies(r, product, customer, qty, on)]
    if not matching:
        price = product.list_price
    else:
        # Paras sääntö ensin: suurin min_qty, sitten tarkin taso, sitten uusin valid_from
        matching.sort(key=lambda r: (_LEVEL[r.scope], r.min_qty, r.valid_from or date.min), reverse=True)
        price = _rule_price(matching[0], product)

    result = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    _cache[cache_key] = result
    return result
