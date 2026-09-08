const { tilaukset_data } = require("./lue_tiedostot");

const jalleenmyyjaOrders = tilaukset_data.filter(
  (order) => order.asiakastyyppi === "jalleenmyyja",
);

const ordersWithUnexpectedDiscount = jalleenmyyjaOrders.filter(
  (order) => order.alennus_pct !== 20,
);

console.log(`Jälleenmyyjätilauksia yhteensä: ${jalleenmyyjaOrders.length}`);
console.log(`Tilauksia, joissa alennus ei ole 20 %: ${ordersWithUnexpectedDiscount.length}`);

for (const order of ordersWithUnexpectedDiscount) {
  console.log(
    `${order.tilaus_id}: ${order.pvm}, ${order.asiakas}, `
    + `alennus_pct=${order.alennus_pct}, summa=${order.summa}`,
  );
}