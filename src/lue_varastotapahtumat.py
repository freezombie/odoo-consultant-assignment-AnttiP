import csv
from datetime import datetime
from pathlib import Path


def read_varasto_tapahtumat(csv_path: Path) -> list[dict[str, object]]:
    """Read warehouse events from a CSV file."""
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        varasto_tapahtumat_data = []

        for row in reader:
            row["maara"] = int(row["maara"]) if row["maara"] else None
            varasto_tapahtumat_data.append(row)

    return varasto_tapahtumat_data


def read_product_box_sizes(csv_path: Path) -> dict[str, int]:
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        return {
            row["sku"]: int(row["kpl_per_ltk"])
            for row in csv.DictReader(csv_file)
        }


def calculate_nivala_balance(
    events: list[dict[str, object]],
    box_sizes: dict[str, int],
    product: str,
    target_time: datetime,
) -> int:
    relevant_events = [
        event for event in events
        if event["tuote"] == product
        and event["tila"] == "vahvistettu"
    ]
    canceled_ids = {
        event["viite"]
        for event in events
        if event["tyyppi"] == "peruutus"
    }
    seen_event_ids: set[str] = set()

    inventory_events = [
        event for event in relevant_events
        if event["tyyppi"] == "inventointi"
        and event["kohde"] == "NIVALA"
        and datetime.fromisoformat(str(event["tapahtuma_aika"])) <= target_time
    ]
    latest_inventory = max(
        inventory_events,
        key=lambda event: datetime.fromisoformat(str(event["tapahtuma_aika"])),
    )
    balance = int(latest_inventory["maara"])
    inventory_time = datetime.fromisoformat(str(latest_inventory["tapahtuma_aika"]))
    print(
        f"Inventory reset at {inventory_time}: "
        f"{balance} {product} in NIVALA"
    )

    for event in sorted(relevant_events, key=lambda item: str(item["id"])):
        event_id = str(event["id"])
        event_time = datetime.fromisoformat(str(event["tapahtuma_aika"]))
        if event is latest_inventory or event_time <= inventory_time or event_time > target_time:
            continue
        if event_id in canceled_ids:
            print(f"SKIP {event_id}: canceled by a peruutus event")
            continue
        if event_id in seen_event_ids:
            print(f"SKIP {event_id}: duplicate event")
            continue
        seen_event_ids.add(event_id)

        quantity = int(event["maara"])
        if event["yksikko"] == "ltk":
            quantity *= box_sizes[product]

        change = 0
        if event["tyyppi"] == "toimitus" and event["lahde"] == "NIVALA":
            change = -quantity
        elif event["tyyppi"] in {"vastaanotto", "palautus"} and event["kohde"] == "NIVALA":
            change = quantity
        elif event["tyyppi"] == "siirto":
            if event["lahde"] == "NIVALA":
                change = -quantity
            elif event["kohde"] == "NIVALA":
                change = quantity

        if change:
            balance += change
            print(f"{event_id}: {change:+d} -> balance {balance}")

    print(f"Final balance at {target_time}: {balance} {product} in NIVALA")
    return balance


varasto_tapahtumat_data = read_varasto_tapahtumat(
    Path(__file__).resolve().parent.parent / "materiaalit" / "varastotapahtumat.csv"
)

if __name__ == "__main__":
    materiaalit_path = Path(__file__).resolve().parent.parent / "materiaalit"
    calculate_nivala_balance(
        varasto_tapahtumat_data,
        read_product_box_sizes(materiaalit_path / "tuotteet.csv"),
        "TUOLI-01",
        datetime(2026, 8, 31, 23, 59, 59),
    )

