"""
show.py - Muestra las lineas sin traducir entre las ids A y B del CSV.
Uso: python show.py A B
"""
import sys, csv

CSV = r"C:\Dev\Default Project\srwv\datos\lineas_batalla.csv"

def main():
    if len(sys.argv) < 3:
        print("uso: python show.py A B")
        sys.exit(1)
    a, b = int(sys.argv[1]), int(sys.argv[2])
    with open(CSV, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = [row for row in r if a <= int(row["id"]) <= b]
    for row in rows:
        es = row["es"]
        pend = "" if es.strip() else "  [SIN TRADUCIR]"
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"{row['id']}|{row['en']}{pend}")

if __name__ == "__main__":
    main()
