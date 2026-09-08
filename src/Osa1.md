Luin varastotapahtumat.csv läpi merkaten tapahtumien tyypit ja tulin siihen
lopputulokseen että on lähdettävä viimeisestä inventointi kohdasta, jossa on
kyseessä TUOLI-01 sekä sijaintina (tarkemmin kohteena) NIVALA. Pyysin VSCoden
Github Copilottia generoimaan python scriptin jossa luetaan varastotapahtumat
listaan. Tämän jälkeen pyysin:

"We need to find out how many TUOLI-01 are in Nivala at 31.8.2026 klo 23:59:59.
We should check how many we have at the beginning i.e everything found at type
inventointi in nivala. Then reduce the ones marked toimitus from Nivala to
somewhere else. Then add the ones marked vastaanotto with the destination being
nivala. Add print logging for each step."

Kaikki rivit ennen E0030 ei laskettu mukaan, koska ne olivat turhia sillä oikea
määrä tulee ilmi kuitenkin välilaskenta inventoinnissa. Rivi E0039 ei laskettu
mukaan, koska se oli duplikaatti.

Vastaus: 23

"Inventory reset at 2026-08-17 09:00:00: 50 TUOLI-01 in NIVALA E0032: -6 ->
balance 44 E0035: -6 -> balance 38 E0039: -7 -> balance 31 SKIP E0039: duplicate
event E0047: +20 -> balance 51 E0048: -8 -> balance 43 E0052: -10 -> balance 33
E0053: -12 -> balance 21 E0055: +2 -> balance 23 Final balance at 2026-08-31
23:59:59: 23 TUOLI-01 in NIVALA"
