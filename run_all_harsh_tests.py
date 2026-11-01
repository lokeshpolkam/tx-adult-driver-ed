import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

test_suites = [
    ('Milestone 1: Clock Timer & Statutory Compliance', 'test_milestone1_harsh.py'),
    ('Milestone 2: Financial, Billing & Stripe Gateway', 'test_milestone2_harsh.py'),
    ('Milestone 3: Examination, Grading & Integrity Bypasses', 'test_milestone3_harsh.py'),
    ('Milestone 4: Certificate Generation & Verification', 'test_milestone4_harsh.py'),
    ('Milestone 5: Authentication, Security & Privacy', 'test_milestone5_harsh.py'),
    ('Milestone 6: Mobile Layout, UX & Forms', 'test_milestone6_harsh.py')
]

print("==========================================================================")
print("RUNNING COMPLETE SUITE OF ALL 6 HARSH ATTACK TESTS")
print("==========================================================================")

all_passed = True

for title, script in test_suites:
    print(f"\n>>> EXECUTING: {title} ({script})")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, encoding='utf-8')
    if result.returncode == 0:
        print(f"✓ {title}: PASSED")
    else:
        print(f"✗ {title}: FAILED!")
        print(result.stdout)
        print(result.stderr)
        all_passed = False
        break

if all_passed:
    print("\n==========================================================================")
    print("ALL 6 MILESTONES PASSED HARSH ATTACK TESTING WITH ZERO VULNERABILITIES!")
    print("==========================================================================")
else:
    print("\nSUITE FAILED. Stopping for investigation.")
    sys.exit(1)
