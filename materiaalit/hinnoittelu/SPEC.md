# Hinnoittelusäännöt — määrittely

Asiakas on huonekaluvalmistaja, joka myy jälleenmyyjille, yrityksille ja kuluttajille. Tarvitaan funktio,
joka palauttaa **yhden tuotteen yksikköhinnan** tietylle asiakkaalle, määrälle ja päivälle.

## Rajapinta

```python
resolve_price(product, customer, qty, on, rules) -> Decimal
```

| Parametri | Tyyppi | Merkitys |
|---|---|---|
| `product` | `Product(sku, list_price)` | `list_price` on listahinta (EUR, ALV 0 %) |
| `customer` | `Customer(id, group_ids)` | asiakas voi kuulua 0…n asiakasryhmään |
| `qty` | `Decimal` | rivin määrä; voi olla murtoluku (esim. 2.5 m kangasta) |
| `on` | `date` | päivä, jonka mukaan hinta määräytyy (yleensä tilauspäivä) |
| `rules` | `list[Rule]` | kaikki järjestelmän hintasäännöt, ei esisuodatettuja |

## Sääntö (`Rule`)

| Kenttä | Merkitys |
|---|---|
| `scope` | `"customer"` (asiakaskohtainen), `"group"` (asiakasryhmä) tai `"all"` (kaikille) |
| `scope_id` | asiakkaan id tai ryhmän id; `None` kun scope on `"all"` |
| `product` | sku, jota sääntö koskee, tai `None` = kaikki tuotteet |
| `min_qty` | sääntö on voimassa, kun `qty >= min_qty` (oletus 0) |
| `valid_from`, `valid_to` | voimassaoloväli, **molemmat päivät mukaan lukien**; `None` = ei rajaa |
| `fixed_price` | kiinteä yksikköhinta — **tai** |
| `discount_pct` | alennusprosentti listahinnasta (`20` = 20 %) |

Säännössä on aina täsmälleen toinen kentistä `fixed_price` / `discount_pct`.

## Valintasäännöt

1. Sääntö on **ehdokas**, jos se koskee tuotetta, koskee asiakasta (scope), `min_qty` täyttyy ja päivä `on` on voimassaolovälillä.
2. **Taso ratkaisee ensin.** Asiakaskohtainen sääntö voittaa ryhmäsäännön, ryhmäsääntö voittaa yleisen. Alemman tason sääntöjä ei katsota lainkaan, jos ylemmällä tasolla on yksikin ehdokas.
3. Saman tason ehdokkaista valitaan se, jonka `min_qty` on suurin.
4. Jos `min_qty` on sama, valitaan se, jonka `valid_from` on myöhäisin (`None` lasketaan vanhimmaksi).
5. Jos ehdokkaita ei ole, hinta on listahinta.
6. Alennus lasketaan aina listahinnasta. Alennuksia ei ketjuteta.
7. Tulos pyöristetään kahteen desimaaliin **kaupallisesti** (puolikas ylöspäin): 18.725 → 18.73.
8. Funktiota kutsutaan paljon (tilausrivien laskenta, verkkokaupan hintanäyttö), joten sen pitää olla nopea.
