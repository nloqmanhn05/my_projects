"""
compare.py - normalize and compare the 7 shipment fields (SI vs BL).

No AI here. Pure, deterministic code.

Usage:
    from compare import compare
    problems = compare(si_fields, bl_fields)
    # [] means "No mismatch detected"

Each problem is a dict:
    {"field": ..., "si": ..., "bl": ..., "issue": "differs" | "missing"}
"""
import re

FIELDS = [
    "shipper",
    "consignee",
    "notify_party",
    "port_of_loading",
    "port_of_discharge",
    "container_count",
    "gross_weight_kg",
]

# Words that don't change who a company is ("ACME LTD" vs "ACME LIMITED")
COMPANY_SUFFIXES = {
    "ltd": "limited",
    "limited": "limited",
    "co": "company",
    "company": "company",
    "corp": "corporation",
    "corporation": "corporation",
    "inc": "incorporated",
    "incorporated": "incorporated",
    "sdn": "sdn",
    "bhd": "bhd",
    "gmbh": "gmbh",
    "llc": "llc",
    "pte": "pte",
}


def _clean_text(value):
    """lowercase, drop punctuation, collapse spaces."""
    v = re.sub(r"[^\w\s]", " ", str(value).casefold())
    return re.sub(r"\s+", " ", v).strip()


def _first_line(value):
    """Keep only the name line. Addresses on later lines are not compared."""
    return str(value).strip().splitlines()[0]


def _norm_company(value):
    """Compare the company NAME only (first line), ignore address lines."""
    words = _clean_text(_first_line(value)).split()
    return " ".join(COMPANY_SUFFIXES.get(w, w) for w in words)


def _norm_port(value):
    """
    'PORT KLANG (WESTPORT), MALAYSIA (MYPKG)' -> 'port klang westport malaysia'
    UN/LOCODE in brackets, like (MYPKG), is removed. It is a code, not a name.
    """
    v = re.sub(r"\(\s*[A-Za-z]{5}\s*\)", " ", str(value))
    return _clean_text(v)


def _norm_count(value):
    """'1 x 40'HC' -> 1.0   |   '3' -> 3.0   |   '3 containers' -> 3.0"""
    m = re.match(r"\s*(\d+)", str(value))
    return float(m.group(1)) if m else None


def _norm_weight(value):
    """'21,577 KG' -> 21577.0   |   '22000' -> 22000.0   |   '22.000,5' is not handled yet"""
    nums = re.sub(r"[^\d.]", "", str(value))
    try:
        return float(nums) if nums else None
    except ValueError:
        return None


def norm(field, value):
    """Clean one value so formatting differences don't look like mismatches."""
    if value is None or str(value).strip() == "":
        return None
    if field in ("shipper", "consignee", "notify_party"):
        return _norm_company(value)
    if field in ("port_of_loading", "port_of_discharge"):
        return _norm_port(value)
    if field == "container_count":
        return _norm_count(value)
    if field == "gross_weight_kg":
        return _norm_weight(value)
    return _clean_text(value)


def compare(si: dict, bl: dict):
    """
    Compare SI (reference) vs BL (draft).
    Returns a list of problem fields. Empty list = No mismatch detected.

    issue = "differs"  -> both have a value, values are different (real mismatch)
    issue = "missing"  -> a value is absent or unreadable (send to human review, not a mismatch)
    """
    problems = []
    for f in FIELDS:
        a, b = norm(f, si.get(f)), norm(f, bl.get(f))
        if a is None or b is None:
            problems.append({"field": f, "si": si.get(f), "bl": bl.get(f), "issue": "missing"})
        elif a != b:
            problems.append({"field": f, "si": si.get(f), "bl": bl.get(f), "issue": "differs"})
    return problems


def summarize(problems):
    """Short text for the report."""
    if not problems:
        return "No mismatch detected"
    lines = []
    for p in problems:
        if p["issue"] == "missing":
            lines.append(f"{p['field']}: value missing (SI: {p['si']} / BL: {p['bl']}) - needs review")
        else:
            lines.append(f"{p['field']}: SI: {p['si']} / BL: {p['bl']}")
    return "\n".join(lines)


# ----------------------------------------------------------------------
# Self-test. Run:  python compare.py
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Real values from email_001
    si_1 = {
        "shipper": "APRIL FAR EAST (M) SDN BHD\n  TOWER 2, AVENUE 5, LEVEL 6; KUALA LUMPUR",
        "consignee": "MOORIM SP CO., LTD\n  656, GANGNAM-DAERO; SEOUL",
        "notify_party": "UAB NOVAKOPA",
        "port_of_loading": "PORT KLANG (WESTPORT), MALAYSIA (MYPKG)",
        "port_of_discharge": "CALLAO, PERU (PECLL)",
        "container_count": "1 x 40'HC",
        "gross_weight_kg": "21,577 KG",
    }
    bl_1 = {
        "shipper": "APRIL FAR EAST (M) SDN BHD\n  TOWER 2, AVENUE 5, LEVEL 6; KUALA LUMPUR",
        "consignee": "MOORIM SP CO., LTD\n  656, GANGNAM-DAERO; SEOUL",
        "notify_party": "UAB NOVAKOPA",
        "port_of_loading": "PORT KLANG (WESTPORT), MALAYSIA (MYPKG)",
        "port_of_discharge": "CALLAO, PERU (PECLL)",
        "container_count": "1 x 40'HC",
        "gross_weight_kg": "21,577 KG",
    }

    tests = []

    # 1. Identical documents -> no mismatch
    tests.append(("identical (email_001)", compare(si_1, bl_1), []))

    # 2. Container count differs (the brief's example)
    bl = {**bl_1, "container_count": "2 x 40'HC"}
    tests.append(("container 1 vs 2", [p["field"] for p in compare(si_1, bl)], ["container_count"]))

    # 3. Weight differs
    bl = {**bl_1, "gross_weight_kg": "22,000 KG"}
    tests.append(("weight differs", [p["field"] for p in compare(si_1, bl)], ["gross_weight_kg"]))

    # 4. Formatting only -> NOT a mismatch
    bl = {**bl_1, "gross_weight_kg": "21577", "shipper": "april far east (m) sdn bhd"}
    tests.append(("formatting only", [p["field"] for p in compare(si_1, bl)], []))

    # 5. Port code removed -> NOT a mismatch
    bl = {**bl_1, "port_of_discharge": "CALLAO, PERU"}
    tests.append(("port code missing", [p["field"] for p in compare(si_1, bl)], []))

    # 6. Different address, same company -> NOT a mismatch
    bl = {**bl_1, "consignee": "MOORIM SP CO., LTD\n  DIFFERENT STREET 1; BUSAN"}
    tests.append(("address differs only", [p["field"] for p in compare(si_1, bl)], []))

    # 7. Different consignee name -> mismatch
    bl = {**bl_1, "consignee": "MOORIM PAPER CO., LTD"}
    tests.append(("consignee name differs", [p["field"] for p in compare(si_1, bl)], ["consignee"]))

    # 8. Missing value -> 'missing', not 'differs'
    bl = {k: v for k, v in bl_1.items() if k != "notify_party"}
    res = compare(si_1, bl)
    tests.append(("missing notify", [(p["field"], p["issue"]) for p in res], [("notify_party", "missing")]))

    # 9. Wrong port -> mismatch
    bl = {**bl_1, "port_of_loading": "PORT KLANG (NORTHPORT), MALAYSIA (MYPKG)"}
    tests.append(("port name differs", [p["field"] for p in compare(si_1, bl)], ["port_of_loading"]))

    passed = 0
    for name, got, expected in tests:
        ok = got == expected
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"      got:      {got}")
            print(f"      expected: {expected}")

    print(f"\n{passed}/{len(tests)} tests passed")
    print("\nExample report for container mismatch:")
    print(summarize(compare(si_1, {**bl_1, "container_count": "2 x 40'HC"})))