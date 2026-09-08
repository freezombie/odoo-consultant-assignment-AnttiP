1. "Me ei koskaan laskuteta ennen toimitusta" ei pidä paikkaansa. Nämä viisi on
   ennen toimitusta:

L26-0003: ennakkolasku for T26-008 on 2026-06-11; linked delivery record(s):
TO26-009 (2026-06-20) L26-0023: ennakkolasku for T26-026 on 2026-07-09; linked
delivery record(s): TO26-032 (2026-07-20) L26-0027: ennakkolasku for T26-030 on
2026-07-15; linked delivery record(s): TO26-035 (2026-07-27) L26-0028:
ennakkolasku for T26-031 on 2026-07-16; linked delivery record(s): TO26-033
(2026-07-22) L26-0040: lasku for T26-039 on 2026-08-04; linked delivery
record(s): TO26-042 (2026-08-11) L26-0016: lasku for T26-019 on 2026-07-01;
linked delivery record(s): none

Ensimmäiseen neljään selitys on että kyseessä on ennakkolaskutus.

Viidennestä en osaa sanoa miksi on laskutettu etukäteen, kyseessä on messut
joten olisikohan kyseessä jonkunnäköinen vuokrasopimus.

Kuudennessa uskoisin että tilaus on noudettu, koska sekä tilaus että lasku ovat
samana päivänä. Toimitusta ei näin ollen tarvittu.

Miten varmistin: Kävin datan läpi, huomasin virheitä tekoälyn päätelmissä ja
korjasin ne oikeaksi. (Ehdotti väärää laskua aluksi, ei ollut yhdistänyt oikein
tilaus_idn kautta kaikki kolme taulua.)

"jälleenmyyjät saa kaikki saman kakskyt prosenttia"

Jälleenmyyjätilauksia yhteensä: 17 Tilauksia, joissa alennus ei ole 20 %: 8
T26-009: 2026-06-12, Kaluste-Kulma Oy, alennus_pct=25, summa=4950 T26-012:
2026-06-18, Huonekaluhalli Lakeus Oy, alennus_pct=0, summa=3750 T26-018:
2026-06-26, Kaluste-kulma Oy, alennus_pct=25, summa=10342.5 T26-020: 2026-06-30,
Kaluste-Kulma Oy, alennus_pct=25, summa=7042.5 T26-022: 2026-07-02,
KALUSTE-KULMA OY, alennus_pct=25, summa=2617.5 T26-030: 2026-07-14, Sisustus
Pohjola Oy, alennus_pct=15, summa=10455 T26-036: 2026-07-28, Kaluste-Kulma Oy,
alennus_pct=25, summa=6337.5 T26-040: 2026-08-04, Sisustus Pohjola Oy,
alennus_pct=15, summa=2635

Kaikilla muilla jälleenmyyjätilauksilla alennusprosentti on 20. Uskoisin että
mahdollisia selityksiä ovat erilaiset alennus prosentit esimerkiksi
kanta-asiakkuuden mukaan, määrä-alennukset sekä nollan prosentin kohdalla ehkä
jopa inhimillinen virhe.

Miten varmistin: Oikeastaan katsoin ensin ihan datasta jalleenmyyja kohtaa ja
heti ensimmäisenä näin että yhdellä oli alennusprosentti nolla. Tästä sitten
tarkistus että millä on nolla. Huomasain kuitenkin vielä myöhemmin että joillain
on myös 25, joten varmistin että otetaan huomioon kaikki joissa alennus ei ole
20%.

## Viesti toimitusjohtajalle

Hei,

Tarkistimme kaksi mainitsemaanne käytäntöä. Datassa on viisi tapausta, joissa
lasku on päivätty ennen ensimmäistä toimitusta: neljä ennakkolaskua ja yksi
tavallinen lasku (`T26-039`). Lisäksi tilauksella `T26-019` on lasku, mutta ei
toimitusriviä. Jälleenmyyjien 17 tilauksesta kahdeksassa alennus poikkeaa 20
prosentista: viidessä alennus on 25 %, kahdessa 15 % ja yhdessä 0 %.

Mikä selittää `T26-039`:n tavallisen laskun ja `T26-019`:n puuttuvan
toimitusrivin? Perustuvatko poikkeavat alennukset mahdollisesti asiakassopimuksiin,
kampanjoihin tai määräalennuksiin, vai onko datassa mahdollisesti
syöttövirheitä?

Ystävällisin terveisin Antti Pikkuaho
