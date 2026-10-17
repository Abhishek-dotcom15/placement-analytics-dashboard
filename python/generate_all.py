"""
End-to-end data generation pipeline runner.
Executes data generation scripts sequentially to maintain referential integrity.
"""

import os
import subprocess
import sys

SCRIPTS = [
    ("generate_companies.py", "1/5 Generating companies..."),
    ("generate_drives.py", "2/5 Generating placement drives..."),
    ("generate_applications.py", "3/5 Generating student applications..."),
    ("generate_interviews.py", "4/5 Generating interview rounds..."),
    ("generate_offers.py", "5/5 Generating placement offers..."),
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 60)
    print("Starting Placement Analytics Data Generation Pipeline")
    print("=" * 60)

    for script_name, description in SCRIPTS:
        script_path = os.path.join(base_dir, script_name)
        print(f"\n[+] {description}")
        result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(base_dir))
        if result.returncode != 0:
            print(f"[!] Error: {script_name} failed with exit code {result.returncode}")
            sys.exit(result.returncode)

    print("\n" + "=" * 60)
    print("[SUCCESS] All recruitment datasets generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
