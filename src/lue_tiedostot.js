const path = require("path");
const { readCsv } = require("./lue_csv");

const materiaalitPath = path.resolve(__dirname, "..", "materiaalit");

const tilaukset_data = readCsv(path.join(materiaalitPath, "tilaukset.csv")).map((row) => ({
  ...row,
  listahinta: Number(row.listahinta),
  alennus_pct: Number(row.alennus_pct),
  summa: Number(row.summa),
}));

const toimitukset_data = readCsv(path.join(materiaalitPath, "toimitukset.csv"));

const laskut_data = readCsv(path.join(materiaalitPath, "laskut.csv")).map((row) => ({
  ...row,
  summa: Number(row.summa),
}));

module.exports = { tilaukset_data, toimitukset_data, laskut_data };