
# Ennakkotehtävä, tunnin versio

> **Hakijalle:** älä julkaise vastauksiasi julkisesti (esim. julkisena forkkina tai gistinä). Palauta ne saatekirjeen ohjeiden mukaan. Materiaali on tarkoitettu vain Softagram Oy:n rekrytointikäyttöön.

Kiitos kiinnostuksestasi. Tämä tehtävä on kolmiosainen ja vie noin tunnin. Se ei vaadi
Odoo-osaamista — perehdytämme Odooseen työn alussa. Osat jäljittelevät sitä, mitä rooli oikeasti
sisältää: tarkkaa päättelyä datasta, asiakkaan prosessin ymmärtämistä ja tekoälyn tuottaman koodin
arviointia, jonka tuloksesta vastaat itse.

## Käytännöt

**Aika.** Noin 60 minuuttia. Älä ylitä sitä olennaisesti; jos aika loppuu, kirjoita mihin jäit ja
mitä tekisit seuraavaksi. Osat ovat toisistaan riippumattomia.

**Tekoäly.** Saat käyttää mitä tahansa työkaluja (Claude, ChatGPT, Copilot, Cursor tai muu). Se on
osa tätä työtä. Vastaat kuitenkin itse tuloksesta. Lisää palautuksen loppuun yksi kohta **”Miten
varmistin”** (3–5 riviä): mitä teit itse, mitä annoit työkalun tehdä, ja mistä tiedät että tulos on
oikein.

**Palautus.** Zip-paketti tai git-repo: vastaukset markdownina, koodi mukana jos käytit sitä.
Palautusaika ja yhteyshenkilö ovat saatekirjeessä. Käytämme palautustasi vain tähän rekrytointiin
ja poistamme sen prosessin päätyttyä.

**Materiaalit** ovat kansiossa `materiaalit/`:

| Tiedosto | Osa |
|---|---|
| `tuotteet.csv`, `varastotapahtumat.csv` | 1 |
| `tilaukset.csv`, `toimitukset.csv`, `laskut.csv` | 2 |
| `hinnoittelu/SPEC.md`, `hinnoittelu/hinnoittelu.py`, `hinnoittelu/test_hinnoittelu.py` | 3 |

Kaikki tiedostoissa esiintyvät yritykset, henkilöt ja luvut ovat keksittyjä.

---

## Osa 1 — Yhden tuotteen saldo (15 min)

Huonekaluvalmistajalla on kaksi varastopaikkaa, **NIVALA** ja **OULU**, eikä se enää luota
varastojärjestelmänsä saldoihin. `varastotapahtumat.csv` on vienti järjestelmän tapahtumalokista
(otettu 4.9.2026), täsmälleen sellaisena kuin se järjestelmästä tuli. Jokaisella rivillä on
tunniste (`id`), `kirjausaika` (milloin rivi tallennettiin järjestelmään), `tapahtuma_aika`
(milloin tavara fyysisesti liikkui tai laskettiin), tyyppi, tuote, määrä ja yksikkö (`kpl` tai
`ltk` = laatikko; laatikkokoot ovat `tuotteet.csv`:ssä), lähde ja kohde, viite sekä tila
(`vahvistettu` tai `luonnos`).

| `tyyppi` | Merkitys |
|---|---|
| `inventointi` | varastossa `kohde` fyysisesti laskettu määrä hetkellä `tapahtuma_aika`; korvaa laskennallisen saldon |
| `vastaanotto` | tavaraa saapuu toimittajalta varastoon `kohde` |
| `toimitus` | tavaraa lähtee varastosta `lahde` asiakkaalle |
| `siirto` | tavaraa siirtyy varastosta `lahde` varastoon `kohde` |
| `palautus` | asiakas palauttaa tavaraa varastoon `kohde` |
| `peruutus` | mitätöi tapahtuman, jonka tunniste on sarakkeessa `viite` |

**Tehtävä.** Laske tuotteen **TUOLI-01** saldo varastossa **NIVALA** hetkellä **31.8.2026 klo
23:59:59**. Listaa lokin rivit, joita et laskenut mukaan sellaisinaan, ja perustele kukin yhdellä
rivillä.

**Palautus:** luku, perustelut ja koodi, jos käytit sitä.

---

## Osa 2 — Kaksi väitettä vastaan data (25 min)

Olet aloittamassa ERP-projektia huonekaluvalmistaja **Havu & Hirsi Oy:n** kanssa (35 työntekijää,
Nivala). Toimitusjohtaja kuvasi tilaus–toimitus–laskutus-prosessin ensimmäisessä tapaamisessa näin:

> ”Meillä tää on aika suoraviivaista. Tilaus tulee myyjälle puhelimella tai sähköpostilla,
> jälleenmyyjiltä yleensä sähköpostilla. Verkkokauppa meillä on, mutta se on tosi pieni juttu, ehkä
> viisi prosenttia, lähinnä yksityisasiakkaita. Myyjä kirjaa tilauksen, tuotanto tekee tai kerää, ja
> kaikki lähtee Nivalan varastosta — meillä ei oo muita varastoja, Oulussa on vaan näyttelytila.
> Kun tavara on lähtenyt, laskutetaan. Me ei koskaan laskuteta ennen toimitusta, se on ollut
> periaate alusta asti, asiakkaat arvostaa sitä. Yksi tilaus, yksi toimitus, yksi lasku — sen takia
> tää on pysynyt hallinnassa Excelillä. Jälleenmyyjät saa kaikki saman kakskyt prosenttia
> listahinnasta, siitä ei neuvotella. Palautuksia ei käytännössä ole, huonekalut on
> mittatilaustyötä.”

Sait heidän nykyjärjestelmästään viennit: tilaukset ajalta 1.6.–31.8.2026 sekä niihin liittyvät
toimitukset ja laskut (vienti otettu 4.9.2026). Summat ovat euroja ilman arvonlisäveroa.

| Tiedosto | Sarakkeet |
|---|---|
| `tilaukset.csv` | `tilaus_id, pvm, asiakas, asiakastyyppi, kanava, listahinta, alennus_pct, summa` |
| `toimitukset.csv` | `toimitus_id, tilaus_id, pvm, lahtopaikka, tila` |
| `laskut.csv` | `lasku_id, tilaus_id, pvm, tyyppi, summa` — `tyyppi` on `lasku`, `ennakkolasku` tai `hyvityslasku` |

**Tehtävä.**

1. Tarkista kaksi väitettä: *”me ei koskaan laskuteta ennen toimitusta”* ja *”jälleenmyyjät saa
   kaikki saman kakskyt prosenttia”*. Kummastakin: pitääkö se paikkansa, mikä on näyttö
   (tunnisteet, lukumäärät), ja **vähintään kaksi mahdollista selitystä** poikkeamille. Älä valitse
   selitystä — et voi vielä tietää.
2. Kirjoita toimitusjohtajalle viesti (enintään 100 sanaa), jossa kerrot havaintosi ja kysyt sen,
   mitä sinun pitää tietää. Hän kuvasi prosessin vilpittömästi.
3. Jos ehdit: mikä muu datassa yllätti sinut? Yksi asia riittää.

**Palautus:** vastaukset markdownina; analyysi koodilla tai taulukkolaskennalla, kumpi tahansa.

---

## Osa 3 — Tekoälyn kirjoittaman koodin katselmointi (20 min)

Kollegasi pyysi AI-koodausagenttia toteuttamaan asiakkaan hinnoittelusäännöt määrittelyn
`hinnoittelu/SPEC.md` pohjalta. Agentti tuotti tiedostot `hinnoittelu.py` ja `test_hinnoittelu.py`,
ja testit menevät läpi. Koodi on menossa huomenna tuotantoon asiakkaan verkkokauppaan. Testit
ajetaan kansiossa `materiaalit/hinnoittelu` komennolla `python -m pytest` (Python 3.10 tai uudempi,
`pytest` asennettuna).

**Tehtävä.**

1. Etsi koodista **vähintään kolme virhettä** suhteessa määrittelyyn, vakavimmat ensin. Kustakin:
   mikä on väärin ja kenelle se näkyy tuotannossa.
2. Kirjoita kullekin löydölle testi, joka **epäonnistuu nykyisellä koodilla**. Korjaa koodi, jos
   ehdit; säilytä rajapinta ennallaan (funktion nimi ja parametrit, dataluokkien nimet ja kentät).
3. Yhdellä tai kahdella lauseella: miksi mukana tulleet testit eivät paljastaneet näitä virheitä?

**Palautus:** löydöslista, testit ja korjattu koodi, jos ehdit.

---

## Mitä arvioimme

- **Tarkkuus.** Tarkistettavat luvut ovat oikein, eikä mitään ole keksitty.
- **Arvostelukyky.** Tiedät, mitä et tiedä. Hypoteesi on hypoteesi, ei johtopäätös.
- **Viestintä.** Asiakkaalle kirjoitettu teksti on ymmärrettävää ilman teknistä taustaa.
- **Rehellisyys.** ”Miten varmistin” kuvaa sitä, mitä oikeasti teit.

Kysymykset ovat tervetulleita — yhteystiedot ovat saatekirjeessä.
