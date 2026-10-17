"""
Placement Analytics Dashboard - Master Project Runner
Executes analytical SQL queries on recruitment datasets and launches the interactive dashboard.
"""

import os
import sys
import webbrowser
import subprocess

try:
    import duckdb
except ImportError:
    print("[*] Installing required duckdb engine...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb"])
    import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")
DASHBOARD_HTML = os.path.join(BASE_DIR, "dashboard", "index.html")

def run_analytics():
    print("=" * 72)
    print("  PLACEMENT ANALYTICS DASHBOARD - EXECUTIVE REPORT")
    print("=" * 72)

    con = duckdb.connect(':memory:')

    # Load schema
    schema_path = os.path.join(SQL_DIR, "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        for stmt in f.read().split(";"):
            if stmt.strip():
                con.execute(stmt)

    # Load datasets
    datasets = [
        ("companies", os.path.join(DATA_DIR, "companies.csv")),
        ("placement_drives", os.path.join(DATA_DIR, "placement_drives.csv")),
        ("students", os.path.join(DATA_DIR, "students.csv")),
        ("applications", os.path.join(DATA_DIR, "applications.csv")),
        ("interview_rounds", os.path.join(DATA_DIR, "interview_rounds.csv")),
        ("offers", os.path.join(DATA_DIR, "offers.csv")),
    ]

    for table_name, csv_path in datasets:
        normalized_path = csv_path.replace("\\", "/")
        con.execute(f"COPY {table_name} FROM '{normalized_path}' (HEADER true);")

    # 1. Executive KPIs
    kpi_res = con.execute("""
        SELECT 
            (SELECT COUNT(*) FROM students) AS total_students,
            (SELECT COUNT(DISTINCT s.student_id) FROM students s JOIN applications a ON s.student_id=a.student_id JOIN offers o ON a.application_id=o.application_id) AS placed_students,
            (SELECT ROUND(100.0 * COUNT(DISTINCT s.student_id) FILTER (WHERE o.offer_id IS NOT NULL) / COUNT(DISTINCT s.student_id), 2) FROM students s LEFT JOIN applications a ON a.student_id=s.student_id LEFT JOIN offers o ON a.application_id=o.application_id) AS placement_rate,
            (SELECT COUNT(*) FROM companies) AS total_companies,
            (SELECT COUNT(*) FROM placement_drives) AS total_drives,
            (SELECT COUNT(*) FROM applications) AS total_applications,
            (SELECT COUNT(*) FROM offers) AS total_offers,
            (SELECT ROUND(AVG(offered_ctc), 2) FROM offers) AS avg_ctc,
            (SELECT MAX(offered_ctc) FROM offers) AS max_ctc
    """).fetchone()

    print("\n[+] EXECUTIVE KPIs:")
    print(f"    * Total Cohort Students  : {kpi_res[0]:,}")
    print(f"    * Students Placed        : {kpi_res[1]:,} ({kpi_res[2]}% Placement Rate)")
    print(f"    * Recruiting Companies   : {kpi_res[3]:,}")
    print(f"    * Total Placement Drives : {kpi_res[4]:,}")
    print(f"    * Applications Submitted : {kpi_res[5]:,}")
    print(f"    * Total Offers Generated : {kpi_res[6]:,}")
    print(f"    * Average Package (CTC)  : {kpi_res[7]} LPA")
    print(f"    * Highest Package (CTC)  : {kpi_res[8]} LPA")

    # 2. Funnel Analysis
    funnel = con.execute("""
        SELECT '1. Applications' AS stage, COUNT(*) AS count FROM applications
        UNION ALL
        SELECT '2. Assessment Cleared (OA >= 70)', COUNT(*) FROM applications WHERE oa_score >= 70
        UNION ALL
        SELECT '3. Reached Interview Rounds', COUNT(DISTINCT application_id) FROM interview_rounds
        UNION ALL
        SELECT '4. Final Offers Generated', COUNT(DISTINCT application_id) FROM offers;
    """).fetchall()

    print("\n[+] RECRUITMENT FUNNEL PROGRESSION:")
    for stage, count in funnel:
        print(f"    {stage:<35} : {count:>7,}")

    # 3. Branch Performance
    branches = con.execute("""
        SELECT 
            b.branch_name,
            COUNT(DISTINCT s.student_id) AS students,
            COUNT(DISTINCT CASE WHEN o.offer_id IS NOT NULL THEN s.student_id END) AS placed,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.offer_id IS NOT NULL THEN s.student_id END) / COUNT(DISTINCT s.student_id), 1) AS pct,
            COUNT(DISTINCT o.offer_id) AS offers,
            ROUND(AVG(o.offered_ctc), 2) AS avg_ctc
        FROM branches b
        JOIN students s ON b.branch_id = s.branch_id
        LEFT JOIN applications a ON s.student_id = a.student_id
        LEFT JOIN offers o ON a.application_id = o.application_id
        GROUP BY b.branch_name
        ORDER BY b.branch_name;
    """).fetchall()

    print("\n[+] BRANCH PLACEMENT BREAKDOWN:")
    print(f"    {'Branch':<12} {'Students':<10} {'Placed':<10} {'Rate':<10} {'Offers':<10} {'Avg CTC':<10}")
    print("    " + "-" * 62)
    for b in branches:
        rate_str = f"{b[3]}%"
        ctc_str = f"{b[5]} LPA"
        print(f"    Branch {b[0]:<5} {b[1]:<10} {b[2]:<10} {rate_str:<10} {b[4]:<10} {ctc_str:<10}")

    # 4. Top Recruiters
    top_cos = con.execute("""
        SELECT 
            c.company_name,
            c.industry,
            COUNT(o.offer_id) AS offers,
            ROUND(AVG(o.offered_ctc), 2) AS avg_ctc
        FROM companies c
        JOIN placement_drives d ON c.company_id = d.company_id
        JOIN applications a ON d.drive_id = a.drive_id
        JOIN offers o ON a.application_id = o.application_id
        GROUP BY c.company_name, c.industry
        ORDER BY offers DESC
        LIMIT 5;
    """).fetchall()

    print("\n[+] TOP 5 RECRUITERS:")
    for co in top_cos:
        print(f"    * {co[0]:<20} ({co[1]:<12}) : {co[2]:>4} offers | Avg: {co[3]} LPA")

    print("\n" + "=" * 72)

def main():
    if "--generate" in sys.argv:
        print("[*] Running synthetic data generation pipeline...")
        gen_script = os.path.join(BASE_DIR, "python", "generate_all.py")
        subprocess.check_call([sys.executable, gen_script])

    run_analytics()

    if "--cli" not in sys.argv:
        if os.path.exists(DASHBOARD_HTML):
            print("\n[+] Launching interactive web dashboard in default browser...")
            webbrowser.open_new_tab(f"file:///{os.path.abspath(DASHBOARD_HTML)}")
            print(f"    Dashboard file: {DASHBOARD_HTML}")
        else:
            print("[!] Dashboard file not found.")

if __name__ == "__main__":
    main()
