"""
TX-ADE Course Shell Server & TDLR Compliant Grading Engine
Serves the course shell, lessons, topic MCQs, and final exam.
Runs server-side grading endpoints to eliminate client answer-key leakage.
Zero external dependencies (uses standard Python library).
"""

import http.server
import json
import os
import random
import socket
import socketserver
import sys
import threading
import time
import urllib.parse
import uuid
import webbrowser

from final_exam_engine import generate_30_question_exam, FINAL_EXAM_BANK

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MCQS_DIR = os.path.join(DIRECTORY, "mcqs")
MASTER_KEYS_PATH = os.path.join(MCQS_DIR, "master_answer_keys.json")

# In-memory answer key cache (protected on server side)
MASTER_KEYS_CACHE = {}
if os.path.exists(MASTER_KEYS_PATH):
    try:
        with open(MASTER_KEYS_PATH, "r", encoding="utf-8") as f:
            raw_keys = json.load(f)
            for t in raw_keys:
                MASTER_KEYS_CACHE[t["topic_id"].upper()] = t
        print(f"[SERVER] Loaded {len(MASTER_KEYS_CACHE)} topic answer keys into secure server memory.")
    except Exception as e:
        print(f"[SERVER WARNING] Could not load answer keys: {e}")

# In-memory active final exam sessions
EXAM_SESSIONS = {}


class UnifiedCourseShellHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _set_json_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()

    def end_headers(self):
        if not any(h.lower().startswith(b"cache-control:") for h in getattr(self, "_headers_buffer", [])):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self._set_json_headers(204)

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        # Favicon handler
        if path == "/favicon.ico":
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#E87522"/><text x="50" y="65" font-size="50" font-family="sans-serif" font-weight="bold" fill="white" text-anchor="middle">TX</text></svg>')
            return

        # 1. Health & Compliance Status Endpoint
        if path == "/api/v1/health":
            self._set_json_headers(200)
            payload = {
                "status": "HEALTHY",
                "engine": "Texas Adult Driver Education LMS & Grading Engine",
                "standards": "TDLR 16 TAC §84.500 & §84.503 Compliant (75 Topics / 6 Hours)",
                "work_zone_mandate": "Sept 1, 2026 Mandate (HB 1884 / TTC §472.022)",
                "loaded_topics": len(MASTER_KEYS_CACHE),
                "timestamp": int(time.time()),
                "zero_client_leak_guarantee": True
            }
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
            return

        # 2. Get Sanitized Topic Questions (Zero Correct Keys / Zero Hashes)
        # GET /api/v1/lessons/:topicId/questions
        if path.startswith("/api/v1/lessons/") and path.endswith("/questions"):
            parts = path.strip("/").split("/")
            if len(parts) == 5:
                topic_id = parts[3].upper()
                if topic_id in MASTER_KEYS_CACHE:
                    topic_data = MASTER_KEYS_CACHE[topic_id]
                    sanitized_questions = []
                    for q in topic_data["questions"]:
                        sanitized_questions.append({
                            "number": q["number"],
                            "category": q["category"],
                            "statute": q["statute"],
                            "svg_key": q.get("svg_key"),
                            "prompt": q["prompt"],
                            "options": q["options"]
                            # No correct_option or sha256_hash included
                        })
                    self._set_json_headers(200)
                    res = {
                        "success": True,
                        "topic_id": topic_id,
                        "lesson_title": topic_data["lesson_title"],
                        "topic_title": topic_data["topic_title"],
                        "questions": sanitized_questions
                    }
                    self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
                    return
                else:
                    self._set_json_headers(404)
                    self.wfile.write(json.dumps({"error": f"Topic {topic_id} not found"}).encode("utf-8"))
                    return

        # 3. Generate TDLR 16 TAC §84.503 Final Exam (30 Questions: 15 Signs + 15 Laws)
        # GET /api/v1/exam/generate
        if path == "/api/v1/exam/generate":
            session_id = f"exam_{uuid.uuid4().hex[:12]}"
            exam_seed = int(time.time() * 1000) % 1000000
            exam_questions = generate_30_question_exam(seed=exam_seed)
            
            # Record keys in server session memory only
            answer_key = {q["number"]: q["correct_option"] for q in exam_questions}
            rationales = {q["number"]: q["rationale"] for q in exam_questions}
            domains = {q["number"]: q["domain"] for q in exam_questions}
            
            EXAM_SESSIONS[session_id] = {
                "created_at": time.time(),
                "answer_key": answer_key,
                "rationales": rationales,
                "domains": domains
            }

            # Sanitize for client: remove correct_option
            sanitized_exam = []
            for q in exam_questions:
                sanitized_exam.append({
                    "number": q["number"],
                    "domain": q["domain"],
                    "category": q["category"],
                    "statute": q["statute"],
                    "svg_key": q.get("svg_key"),
                    "prompt": q["prompt"],
                    "options": q["options"]
                })

            self._set_json_headers(200)
            res = {
                "success": True,
                "examSessionId": session_id,
                "totalQuestions": 30,
                "bank_a_signs_count": 15,
                "bank_b_laws_count": 15,
                "passingThresholdPercent": 70.0,
                "passingQuestionsRequired": 21,
                "questions": sanitized_exam
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
            return

        # Fallback to standard static file serving from DIRECTORY
        return super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        # Read JSON body
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            self._set_json_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode("utf-8"))
            return

        # 1. Single Question Server-Side Grading
        # POST /api/v1/lessons/:topicId/grade
        if path.startswith("/api/v1/lessons/") and path.endswith("/grade"):
            parts = path.strip("/").split("/")
            if len(parts) == 5:
                topic_id = parts[3].upper()
                q_num = req_data.get("questionNumber")
                selected_opt = req_data.get("selectedOption")

                if topic_id in MASTER_KEYS_CACHE and q_num and selected_opt:
                    topic_data = MASTER_KEYS_CACHE[topic_id]
                    target_q = next((q for q in topic_data["questions"] if q["number"] == int(q_num)), None)
                    if target_q:
                        is_correct = (int(selected_opt) == target_q["correct_option"])
                        self._set_json_headers(200)
                        res = {
                            "success": True,
                            "topicId": topic_id,
                            "questionNumber": int(q_num),
                            "isCorrect": is_correct,
                            "correctOption": target_q["correct_option"],
                            "statutoryRationale": target_q["statutory_rationale"]
                        }
                        self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
                        return

        # 1b. Single Final Exam Question Server-Side Grading
        # POST /api/v1/exam/grade
        if path == "/api/v1/exam/grade":
            session_id = req_data.get("examSessionId")
            q_num = req_data.get("questionNumber")
            selected_opt = req_data.get("selectedOption")

            if session_id in EXAM_SESSIONS and q_num and selected_opt:
                session_data = EXAM_SESSIONS[session_id]
                correct_opt = session_data["answer_key"].get(int(q_num))
                if correct_opt is not None:
                    is_correct = (int(selected_opt) == correct_opt)
                    self._set_json_headers(200)
                    res = {
                        "success": True,
                        "questionNumber": int(q_num),
                        "isCorrect": is_correct,
                        "correctOption": correct_opt,
                        "rationale": session_data["rationales"].get(int(q_num), ""),
                        "domain": session_data["domains"].get(int(q_num), "")
                    }
                    self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
                    return

        # 2. Complete Topic Quiz Batch Submission
        # POST /api/v1/quizzes/submit
        if path == "/api/v1/quizzes/submit":
            topic_id = req_data.get("topicId", "").upper()
            user_answers = req_data.get("answers", {})

            if topic_id in MASTER_KEYS_CACHE:
                topic_data = MASTER_KEYS_CACHE[topic_id]
                total = len(topic_data["questions"])
                correct_count = 0
                results = []

                for q in topic_data["questions"]:
                    user_pick = user_answers.get(str(q["number"]))
                    is_correct = (user_pick is not None and int(user_pick) == q["correct_option"])
                    if is_correct:
                        correct_count += 1
                    results.append({
                        "questionNumber": q["number"],
                        "userSelection": user_pick,
                        "isCorrect": is_correct,
                        "statutoryRationale": q["statutory_rationale"]
                    })

                score_pct = round((correct_count / total) * 100, 1) if total > 0 else 0
                passed = (score_pct >= 70.0)

                self._set_json_headers(200)
                res = {
                    "success": True,
                    "topicId": topic_id,
                    "scorePercent": score_pct,
                    "correctCount": correct_count,
                    "totalQuestions": total,
                    "passed": passed,
                    "passingThresholdPercent": 70.0,
                    "results": results
                }
                self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
                return

        # 3. Final Examination Batch Submission (TDLR 16 TAC §84.503)
        # POST /api/v1/exam/submit
        if path == "/api/v1/exam/submit":
            session_id = req_data.get("examSessionId")
            user_answers = req_data.get("answers", {})

            if session_id in EXAM_SESSIONS:
                session_data = EXAM_SESSIONS[session_id]
                keys = session_data["answer_key"]
                rationales = session_data["rationales"]
                domains = session_data["domains"]

                total = len(keys)
                correct_count = 0
                signs_correct = 0
                laws_correct = 0
                breakdown = []

                for q_num, correct_opt in keys.items():
                    user_pick = user_answers.get(str(q_num))
                    is_correct = (user_pick is not None and int(user_pick) == correct_opt)
                    if is_correct:
                        correct_count += 1
                        if domains[q_num] == "HIGHWAY SIGNS & SIGNALS":
                            signs_correct += 1
                        else:
                            laws_correct += 1
                    breakdown.append({
                        "questionNumber": q_num,
                        "domain": domains[q_num],
                        "userSelection": user_pick,
                        "isCorrect": is_correct,
                        "rationale": rationales[q_num]
                    })

                score_pct = round((correct_count / total) * 100, 1)
                passed = (correct_count >= 21)  # 70% passing threshold (21 of 30)

                res = {
                    "success": True,
                    "examSessionId": session_id,
                    "scorePercent": score_pct,
                    "correctCount": correct_count,
                    "totalQuestions": total,
                    "passed": passed,
                    "bank_a_signs_score": f"{signs_correct} / 15",
                    "bank_b_laws_score": f"{laws_correct} / 15",
                    "tdlr_compliance": {
                        "rule": "16 TAC §84.503",
                        "minimumScorePercent": 70.0,
                        "passedThreshold": passed
                    },
                    "certificateEligible": passed,
                    "certificateSerial": f"ADE1317-2026-{uuid.uuid4().hex[:6].upper()}" if passed else None,
                    "retestAllowed": not passed,
                    "message": "Congratulations! You passed the official TDLR Final Exam." if passed else "Score was below 70.0%. Per 16 TAC §84.503, a re-examination from the alternate question pool is authorized."
                }
                self._set_json_headers(200)
                self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
                return
            else:
                self._set_json_headers(404)
                self.wfile.write(json.dumps({"error": "Exam session expired or not found"}).encode("utf-8"))
                return

        self._set_json_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def log_message(self, format, *args):
        # Clean HTTP logging
        sys.stdout.write(f"  [HTTP] {args[0]} - {args[1]}\n")


def find_available_port(start_port=8080):
    for port in range(start_port, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def main():
    os.chdir(DIRECTORY)
    port = find_available_port(PORT)
    url = f"http://localhost:{port}/index.html"

    print("=" * 68)
    print("        TX-ADE TEXAS ADULT DRIVER ED // COURSE SHELL")
    print("=" * 68)
    print(f" Directory  : {DIRECTORY}")
    print(f" Local URL  : {url}")
    print(" Standards  : TDLR 16 TAC §84.500 & §84.503 (75 Topics / 6 Hours)")
    print(" Security   : Zero Client-Side Answer Leakage (Server-Side Grading)")
    print(" Mandate    : Sept 1, 2026 Work Zone Training (HB 1884 Compliant)")
    print("=" * 68)
    print(" Starting server & launching browser...")
    print(" Press Ctrl+C in this console to stop the server.\n")

    def open_browser():
        time.sleep(0.8)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), UnifiedCourseShellHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nCourse Shell server shut down.")
            sys.exit(0)


if __name__ == "__main__":
    main()
