"""
test_course_shell.py
Comprehensive test suite verifying TX-ADE Course Shell in C:\\tx_dmv\\course_shell:
1. Static files serving (index.html, course-shell.html, mcqs/L01-T01.html, mcqs/final_exam.html, modular questions).
2. Health & TDLR compliance check.
3. Zero answer key leakage in client questions.
4. Server-side single question grading.
5. Server-side full topic batch grading.
6. 30-question TDLR Final Exam generation (15 Bank A signs + 15 Bank B laws).
7. Server-side final exam grading & certificate generation.
"""

import json
import os
import socket
import socketserver
import threading
import time
import urllib.request
import urllib.error

import serve

TEST_PORT = 8092

def run_tests():
    os.chdir(serve.DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", TEST_PORT), serve.UnifiedCourseShellHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    base = f"http://127.0.0.1:{TEST_PORT}"
    print(f"\n[TEST SUITE] Testing Course Shell at {base} ...\n")

    passed_tests = 0
    total_tests = 0

    def assert_eq(desc, actual, expected):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if actual == expected:
            print(f"  [PASS] {desc}: {actual}")
            passed_tests += 1
        else:
            print(f"  [FAIL] {desc}: got '{actual}', expected '{expected}'")
            raise AssertionError(f"{desc} failed")

    def assert_true(desc, condition):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            print(f"  [PASS] {desc}")
            passed_tests += 1
        else:
            print(f"  [FAIL] {desc}")
            raise AssertionError(f"{desc} failed")

    # 1. Health Endpoint
    req = urllib.request.Request(f"{base}/api/v1/health")
    with urllib.request.urlopen(req) as r:
        assert_eq("Health Status Code", r.status, 200)
        data = json.loads(r.read().decode("utf-8"))
        assert_eq("Health API status", data.get("status"), "HEALTHY")
        assert_eq("Loaded topics count", data.get("loaded_topics"), 75)
        assert_true("Zero client leak guarantee", data.get("zero_client_leak_guarantee") is True)

    # 2. Static File: index.html & course-shell.html
    req = urllib.request.Request(f"{base}/index.html")
    with urllib.request.urlopen(req) as r:
        assert_eq("index.html Status Code", r.status, 200)
        content = r.read().decode("utf-8")
        assert_true("index.html contains TAKE A TEST ON THIS TOPIC", "TAKE A TEST ON THIS TOPIC" in content)
        assert_true("index.html contains topic-test-modal", "topic-test-modal" in content)
        assert_true("index.html contains 06:00:00 timer in shell header", "06:00:00" in content)

    # 3. Static File: mcqs/L01-T01.html
    req = urllib.request.Request(f"{base}/mcqs/L01-T01.html")
    with urllib.request.urlopen(req) as r:
        assert_eq("mcqs/L01-T01.html Status Code", r.status, 200)
        content = r.read().decode("utf-8")
        assert_true("Topic MCQ has NO 06:00:00 timer", "06:00:00" not in content)
        assert_true("Topic MCQ has NO DPS Official Knowledge Test claim", "DPS Official Knowledge Test" not in content)
        assert_true("Topic MCQ has NO DPS ROAD TEST STANDARD claim", "DPS ROAD TEST STANDARD" not in content)

    # 4. Static File: mcqs/final_exam.html
    req = urllib.request.Request(f"{base}/mcqs/final_exam.html")
    with urllib.request.urlopen(req) as r:
        assert_eq("final_exam.html Status Code", r.status, 200)
        content = r.read().decode("utf-8")
        assert_true("Final exam mentions 16 TAC §84.503", "84.503" in content)
        assert_true("Final exam has NO 06:00:00 timer", "06:00:00" not in content)

    # 4b. Lesson File: final_course_export/L01-T02.html (Standalone Check)
    req = urllib.request.Request(f"{base}/final_course_export/L01-T02.html")
    with urllib.request.urlopen(req) as r:
        assert_eq("L01-T02.html Status Code", r.status, 200)
        content = r.read().decode("utf-8")
        assert_true("L01-T02 has NO duplicate sidebar (ml-[280px])", "ml-[280px]" not in content)
        assert_true("L01-T02 has NO duplicate syllabus sidebar", "CURRICULUM SYLLABUS" not in content)
        assert_true("L01-T02 has NO duplicate header timer", "04:35:10" not in content)
        assert_true("L01-T02 has standalone main canvas", "max-w-5xl mx-auto" in content)
        assert_true("L01-T02 preserves interactive scripts", "pillarData" in content)

    # 5. Modular MCQ Questions
    req = urllib.request.Request(f"{base}/mcqs/modular_mcqs/questions/L01-T01_Q1.json")
    with urllib.request.urlopen(req) as r:
        assert_eq("Modular question JSON Status Code", r.status, 200)
        qdata = json.loads(r.read().decode("utf-8"))
        assert_eq("Question ID", qdata.get("id"), "L01-T01-Q1")
        assert_true("No correct_option in modular JSON", "correct_option" not in qdata)
        assert_true("No sha256_hash in modular JSON", "sha256_hash" not in qdata)

    # 6. Sanitized Topic Questions via API
    req = urllib.request.Request(f"{base}/api/v1/lessons/L01-T01/questions")
    with urllib.request.urlopen(req) as r:
        assert_eq("Questions API Status Code", r.status, 200)
        qdata = json.loads(r.read().decode("utf-8"))
        assert_eq("Topic ID", qdata.get("topic_id"), "L01-T01")
        questions = qdata.get("questions", [])
        assert_eq("Question count", len(questions), 5)
        for q in questions:
            assert_true("No correct_option in API question", "correct_option" not in q)
            assert_true("No hash in API question", "sha256_hash" not in q)

    # 7. Single Question Grading via API
    grade_payload = json.dumps({"questionNumber": 1, "selectedOption": 2}).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/v1/lessons/L01-T01/grade", data=grade_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        assert_eq("Grade API Status Code", r.status, 200)
        gdata = json.loads(r.read().decode("utf-8"))
        assert_true("isCorrect is boolean", isinstance(gdata.get("isCorrect"), bool))
        assert_true("correctOption returned by server", isinstance(gdata.get("correctOption"), int))
        assert_true("Statutory rationale returned", len(gdata.get("statutoryRationale", "")) > 10)

    # 8. Final Exam Generation (30 Questions: 15 Signs + 15 Laws)
    req = urllib.request.Request(f"{base}/api/v1/exam/generate")
    with urllib.request.urlopen(req) as r:
        assert_eq("Exam Generate Status Code", r.status, 200)
        edata = json.loads(r.read().decode("utf-8"))
        exam_id = edata.get("examSessionId")
        assert_true("Exam session created", exam_id is not None)
        assert_eq("Exam questions total", edata.get("totalQuestions"), 30)
        assert_eq("Bank A signs count", edata.get("bank_a_signs_count"), 15)
        assert_eq("Bank B laws count", edata.get("bank_b_laws_count"), 15)
        exam_qs = edata.get("questions", [])
        for eq in exam_qs:
            assert_true("No correct_option in exam client questions", "correct_option" not in eq)

    # 9. Final Exam Single Question Grade
    exam_grade_payload = json.dumps({
        "examSessionId": exam_id,
        "questionNumber": 1,
        "selectedOption": 1
    }).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/v1/exam/grade", data=exam_grade_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        assert_eq("Exam Grade API Status Code", r.status, 200)
        egdata = json.loads(r.read().decode("utf-8"))
        assert_true("Exam isCorrect is boolean", isinstance(egdata.get("isCorrect"), bool))
        assert_true("Exam rationale provided", len(egdata.get("rationale", "")) > 10)

    # 10. Final Exam Batch Submission & Passing Certificate
    # Fetch correct keys directly from server memory to test passing score
    session_keys = serve.EXAM_SESSIONS[exam_id]["answer_key"]
    submit_payload = json.dumps({
        "examSessionId": exam_id,
        "answers": {str(k): v for k, v in session_keys.items()}
    }).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/v1/exam/submit", data=submit_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        assert_eq("Exam Submit API Status Code", r.status, 200)
        sdata = json.loads(r.read().decode("utf-8"))
        assert_eq("Exam perfect score", sdata.get("scorePercent"), 100.0)
        assert_true("Exam passed", sdata.get("passed") is True)
        assert_true("Certificate serial issued", sdata.get("certificateSerial") is not None)
        assert_true("Certificate serial format", sdata.get("certificateSerial", "").startswith("ADE1317-2026-"))

    httpd.shutdown()
    print("\n" + "=" * 60)
    print(f" ALL {passed_tests} / {total_tests} COURSE SHELL INTEGRATION TESTS PASSED! ")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_tests()
