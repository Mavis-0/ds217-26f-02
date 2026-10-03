"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic reading from every usable encounter."""
    # TODO: collect the systolic value of every encounter into one list.
    readings = []

    for encounter in encounters:
        readings.append(encounter[2])
    return readings


def mean_systolic(readings):
    """Return the mean reading, or None if the list is empty."""
    # TODO: return None when there is nothing to average, then sum() / len().

    if len(readings) == 0:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in usable encounters."""
    # TODO: collect the patient IDs and keep only the distinct ones.
    patient_ids = set()

    for encounter in encounters:
        patient_ids.add(encounter[0])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return unique patient IDs with a reading at or above the cutoff."""
    patient_ids = set()

    for encounter in encounters:
        if encounter[2] >= cutoff:
            patient_ids.add(encounter[0])

    return sorted(patient_ids)
