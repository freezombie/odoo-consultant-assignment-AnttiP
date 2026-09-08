const {
  tilaukset_data,
  toimitukset_data,
  laskut_data,
} = require("./lue_tiedostot");

const deliveriesByOrder = new Map();
for (const delivery of toimitukset_data) {
  if (delivery.tila !== "toimitettu") {
    continue;
  }
  const deliveries = deliveriesByOrder.get(delivery.tilaus_id) ?? [];
  deliveries.push(delivery);
  deliveriesByOrder.set(delivery.tilaus_id, deliveries);
}

const invoicesWithNoDelivery = laskut_data.filter((invoice) => {
  if (invoice.tyyppi === "hyvityslasku") {
    return false;
  }
  const deliveries = deliveriesByOrder.get(invoice.tilaus_id) ?? [];
  return deliveries.length === 0;
});

const invoicesBeforeDelivery = laskut_data.filter((invoice) => {
  if (invoice.tyyppi === "hyvityslasku") {
    return false;
  }
  const deliveries = deliveriesByOrder.get(invoice.tilaus_id) ?? [];
  return deliveries.length > 0
    && deliveries.every((delivery) => invoice.pvm < delivery.pvm);
});

console.log(`Orders loaded: ${tilaukset_data.length}`);
console.log(`Deliveries loaded: ${toimitukset_data.length}`);
console.log(`Invoices loaded: ${laskut_data.length}`);
console.log(`Invoices before delivery: ${invoicesBeforeDelivery.length}`);
console.log(`Invoices with no delivery record: ${invoicesWithNoDelivery.length}`);

for (const invoice of invoicesBeforeDelivery) {
  const deliveries = deliveriesByOrder.get(invoice.tilaus_id) ?? [];
  const deliveryDates = deliveries.length === 0
    ? "none"
    : deliveries.map((delivery) => `${delivery.toimitus_id} (${delivery.pvm})`).join(", ");
  console.log(
    `${invoice.lasku_id}: ${invoice.tyyppi} for ${invoice.tilaus_id} `
    + `on ${invoice.pvm}; linked delivery record(s): ${deliveryDates}`,
  );
}

for (const invoice of invoicesWithNoDelivery) {
  console.log(
    `${invoice.lasku_id}: ${invoice.tyyppi} for ${invoice.tilaus_id} `
    + `on ${invoice.pvm}; linked delivery record(s): none`,
  );
}

console.log(
  invoicesBeforeDelivery.length === 0
    ? "Statement is supported by this data."
    : "Statement is false: at least one invoice predates delivery.",
);