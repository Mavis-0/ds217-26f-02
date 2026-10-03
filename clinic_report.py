#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return usable (patient_id, visit_date, systolic) tuples and a skipped count."""
    encounters = []
    skipped = 0

    with open(data_path, encoding="utf-8") as file:
        next(file, None)

        for line in file:
            line = line.strip()

            if line == "":
                print("Skipping a blank row.")
                skipped += 1
                continue

            fields = line.split(",")

            if len(fields) != 3:
                print(f"Skipping row with wrong number of fields: {line}")
                skipped += 1
                continue

            patient_id, visit_date, systolic_text = fields

            try:
                systolic = int(systolic_text)
            except ValueError:
                print(f"Skipping row with non-integer systolic: {line}")
                skipped += 1
                continue

            if systolic < 60 or systolic > 250:
                print(f"Skipping row with out-of-range systolic: {line}")
                skipped += 1
                continue

            encounters.append((patient_id, visit_date, systolic))

    return encounters, skipped


def main():
    """Write the blood pressure summary and print it."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)
    average = mean_systolic(readings)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {average:.2f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "vitals_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines) + "\n")

    with open(report_path, encoding="utf-8") as file:
        print(file.read())




    cutoff = 145
    reason = (
        "I chose 145 mmHg to include  patients with elevated readings "
        "for follow-up."
    )

    followup_ids = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ]
    followup_lines.extend(followup_ids)

    followup_path = OUTPUT_DIR / "followup_list.txt"

    with open(followup_path, "w", encoding="utf-8") as file:
        file.write("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()
