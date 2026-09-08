Tämän osan tein täysin AIn avulla, sillä aika oli jo loppumassa kesken. Sen tekemät huomiot vaikuttavat kumminkin oikealta.

# Osa 3 — Hinnoittelukoodin katselmointi

## Löydökset

1. **Välimuisti oli liian suppea.** Hinta välimuistettiin vain SKU:n
   perusteella. Asiakas, määrä, päivä ja säännöt jäivät avaimesta pois, joten
   yhden kyselyn hinta saattoi näkyä toiselle asiakkaalle tai toisella määrällä.
   Korjattu käyttämällä koko kyselykontekstia ja sääntöjoukkoa avaimena.

2. **Sääntöjen tasojärjestys oli väärä.** Koodi vertasi ensin määrää ja vasta
   sitten tasoa. Suuremman määrärajan ryhmäsääntö saattoi voittaa
   asiakaskohtaisen säännön, vaikka asiakastason pitää aina voittaa. Korjattu
   järjestämällä taso ensin.

3. **Määräraja oli väärin rajattu.** SPEC sanoo `qty >= min_qty`, mutta koodi
   vaati `qty > min_qty`. Korjattu.

4. **Voimassaolopäivät olivat väärin rajattu.** `valid_from=None` aiheutti
   vertailuvirheen, ja `valid_to` käsiteltiin poissulkevana. SPEC:n mukaan alku-
   ja loppupäivä ovat mukana ja `None` tarkoittaa rajauksen puuttumista.
   Korjattu.

5. **Pyöristys ei ollut kaupallinen.** Float-muunnos ja Pythonin `round`
   käyttivät väärää pyöristyskäyttäytymistä. Korvattu Decimal-arvon
   `ROUND_HALF_UP`-pyöristyksellä.

6. **Virheellinen sääntö jäi epäselväksi.** Jos säännössä ei ollut kumpaakaan
   hintakenttää, koodi päätyi tyyppiongelmaan. Nyt se nostaa selkeän
   `ValueError`-virheen.

## Testit

`test_hinnoittelu.py` sisältää regressiotestit välimuistille,
tasojärjestykselle, määrärajan rajatapaukselle, puuttuville ja päättyville
päivämäärille sekä kaupalliselle pyöristykselle.

Alkuperäiset testit eivät paljastaneet virheitä, koska ne käyttivät vain yhtä
kyselyä tuotetta kohden, eivät testanneet sääntöjen ristiriitaista
tasojärjestystä tai raja-arvoja, ja käyttivät aina määriteltyjä päivämääriä sekä
sellaisia hintoja, joissa pyöristysero ei tullut näkyviin.
