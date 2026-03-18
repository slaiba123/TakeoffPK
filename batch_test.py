import requests
import csv
import time
from datetime import datetime

# ============================================================
# BATCH TEST SCRIPT FOR VISAYAAR BOT
# Run app.py first, then run this script in a second terminal
# Results saved to: test_results_<timestamp>.csv
# ============================================================

BASE_URL = "http://localhost:8080/get"

# ============================================================
# TEST QUESTIONS WITH EXPECTED KEYWORDS
# If ANY keyword is found in the answer → PASS
# ============================================================

test_cases = [

    # ── UK ──────────────────────────────────────────────────
    {
        "country": "UK",
        "level": "General",
        "question": "What documents do I need for a UK student visa as a Pakistani student?",
        "keywords": ["CAS", "passport", "financial", "IELTS", "Confirmation of Acceptance"]
    },
    {
        "country": "UK",
        "level": "General",
        "question": "What is a CAS number and how do I get it?",
        "keywords": ["CAS", "Confirmation of Acceptance", "university", "sponsor"]
    },
    {
        "country": "UK",
        "level": "General",
        "question": "How much money do I need to show for a UK student visa?",
        "keywords": ["1,334", "1334", "680", "London", "outside London"]
    },
    {
        "country": "UK",
        "level": "General",
        "question": "Can I work part time on a UK student visa?",
        "keywords": ["20 hours", "20hrs", "term time", "vacation", "part-time"]
    },
    {
        "country": "UK",
        "level": "UG vs PG",
        "question": "What is the difference between UK student visa for undergrad and postgrad?",
        "keywords": ["undergraduate", "postgraduate", "CAS", "research", "PhD"]
    },

    # ── CANADA ──────────────────────────────────────────────
    {
        "country": "Canada",
        "level": "General",
        "question": "What is a PAL letter and do I need it for Canada study permit?",
        "keywords": ["PAL", "Provincial Attestation", "mandatory", "required"]
    },
    {
        "country": "Canada",
        "level": "General",
        "question": "How much funds do I need to show for Canada study permit in 2025?",
        "keywords": ["22,895", "22895"]  # must show updated 2025 amount
    },
    {
        "country": "Canada",
        "level": "General",
        "question": "What happened to Student Direct Stream for Pakistani students?",
        "keywords": ["discontinued", "November 2024", "no longer", "ended", "cancelled"]
    },
    {
        "country": "Canada",
        "level": "General",
        "question": "What documents do I need for Canada study permit application?",
        "keywords": ["Letter of Acceptance", "LOA", "passport", "IELTS", "financial"]
    },
    {
        "country": "Canada",
        "level": "General",
        "question": "Can I apply for Canada study permit without IELTS?",
        "keywords": ["IELTS", "English", "language", "waiver", "exempt"]
    },

    # ── GERMANY ─────────────────────────────────────────────
    {
        "country": "Germany",
        "level": "General",
        "question": "Is studying in Germany free for Pakistani students?",
        "keywords": ["free", "tuition", "public", "semester fee", "no tuition"]
    },
    {
        "country": "Germany",
        "level": "General",
        "question": "What is a blocked account and how much money do I need for Germany student visa?",
        "keywords": ["blocked account", "Sperrkonto", "11,208", "11208", "934"]
    },
    {
        "country": "Germany",
        "level": "PhD",
        "question": "What is the difference between Germany student visa and PhD visa?",
        "keywords": ["PhD", "doctorate", "research", "supervisor", "student visa"]
    },
    {
        "country": "Germany",
        "level": "General",
        "question": "How do I apply for DAAD scholarship as a Pakistani student?",
        "keywords": ["DAAD", "scholarship", "apply", "portal", "deadline"]
    },

    # ── AUSTRALIA ───────────────────────────────────────────
    {
        "country": "Australia",
        "level": "General",
        "question": "What is student visa subclass 500 for Australia?",
        "keywords": ["500", "subclass", "student visa", "study"]
    },
    {
        "country": "Australia",
        "level": "General",
        "question": "How much money do I need to show for Australia student visa?",
        "keywords": ["21,041", "21041", "AUD", "financial"]
    },
    {
        "country": "Australia",
        "level": "General",
        "question": "What are the health insurance requirements for Australia student visa?",
        "keywords": ["OSHC", "health insurance", "Overseas Student Health Cover"]
    },
    {
        "country": "Australia",
        "level": "General",
        "question": "What is GTE requirement for Australia student visa?",
        "keywords": ["GTE", "Genuine Temporary Entrant", "genuine"]
    },

    # ── USA ─────────────────────────────────────────────────
    {
        "country": "USA",
        "level": "General",
        "question": "What documents do I need for F1 visa as a Pakistani student?",
        "keywords": ["I-20", "SEVIS", "DS-160", "passport", "financial"]
    },
    {
        "country": "USA",
        "level": "General",
        "question": "What is an I-20 form and who issues it?",
        "keywords": ["I-20", "university", "institution", "SEVIS", "issued"]
    },
    {
        "country": "USA",
        "level": "General",
        "question": "How do I pay the SEVIS fee for F1 visa?",
        "keywords": ["SEVIS", "fee", "350", "$350", "pay", "FMJfee"]
    },
    {
        "country": "USA",
        "level": "General",
        "question": "Where can Pakistani students apply for F1 visa?",
        "keywords": ["Islamabad", "Karachi", "Lahore", "Peshawar", "embassy", "consulate"]
    },
    {
        "country": "USA",
        "level": "PhD",
        "question": "What is OPT and can Pakistani PhD students apply?",
        "keywords": ["OPT", "Optional Practical Training", "work", "STEM", "12 months", "24 months"]
    },

    # ── TURKEY ──────────────────────────────────────────────
    {
        "country": "Turkey",
        "level": "General",
        "question": "How do I apply for Türkiye Burslari scholarship as a Pakistani student?",
        "keywords": ["Türkiye Burslari", "scholarship", "apply", "portal", "tbbs"]
    },
    {
        "country": "Turkey",
        "level": "General",
        "question": "What documents do I need for Turkey student visa from Pakistan?",
        "keywords": ["passport", "acceptance", "financial", "insurance", "photo"]
    },

    # ── SAUDI ARABIA ────────────────────────────────────────
    {
        "country": "Saudi Arabia",
        "level": "General",
        "question": "Can Pakistani students study in Saudi Arabia?",
        "keywords": ["Saudi", "study", "university", "scholarship", "Pakistan"]
    },

    # ── CROSS COUNTRY ───────────────────────────────────────
    {
        "country": "Cross-Country",
        "level": "Comparison",
        "question": "Which country offers free education for Pakistani students?",
        "keywords": ["Germany", "free", "tuition", "public university"]
    },
    {
        "country": "Cross-Country",
        "level": "Comparison",
        "question": "Which country is best for PhD with full funding for Pakistanis?",
        "keywords": ["Germany", "USA", "UK", "funding", "scholarship", "assistantship", "stipend"]
    },
]

# ============================================================
# RUN TESTS
# ============================================================

def run_test(test):
    try:
        response = requests.post(BASE_URL, data={"msg": test["question"]}, timeout=60)
        answer = response.text.strip()
        
        # Check if any keyword found in answer (case insensitive)
        found_keywords = [kw for kw in test["keywords"] if kw.lower() in answer.lower()]
        passed = len(found_keywords) > 0
        
        return {
            "country": test["country"],
            "level": test["level"],
            "question": test["question"],
            "answer": answer,
            "expected_keywords": ", ".join(test["keywords"]),
            "found_keywords": ", ".join(found_keywords),
            "result": "✅ PASS" if passed else "❌ FAIL"
        }
    except requests.exceptions.ConnectionError:
        return {
            "country": test["country"],
            "level": test["level"],
            "question": test["question"],
            "answer": "ERROR: Could not connect to app. Make sure app.py is running on port 8080",
            "expected_keywords": ", ".join(test["keywords"]),
            "found_keywords": "",
            "result": "⚠️ ERROR"
        }
    except Exception as e:
        return {
            "country": test["country"],
            "level": test["level"],
            "question": test["question"],
            "answer": f"ERROR: {str(e)}",
            "expected_keywords": ", ".join(test["keywords"]),
            "found_keywords": "",
            "result": "⚠️ ERROR"
        }


def main():
    print("=" * 60)
    print("🧪 VisaYaar Batch Test Starting...")
    print(f"📡 Testing against: {BASE_URL}")
    print(f"📋 Total questions: {len(test_cases)}")
    print("=" * 60)
    print("Make sure app.py is running before proceeding!")
    print()

    results = []
    passed = 0
    failed = 0
    errors = 0

    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] {test['country']} — {test['question'][:60]}...")
        result = run_test(test)
        results.append(result)

        if "PASS" in result["result"]:
            passed += 1
            print(f"  {result['result']} (found: {result['found_keywords']})")
        elif "FAIL" in result["result"]:
            failed += 1
            print(f"  {result['result']} (expected one of: {result['expected_keywords']})")
        else:
            errors += 1
            print(f"  {result['result']}")

        # Small delay to avoid overwhelming the server
        time.sleep(2)

    # ── Save results to CSV ──────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "result", "country", "level", "question",
            "answer", "expected_keywords", "found_keywords"
        ])
        writer.writeheader()
        writer.writerows(results)

    # ── Print Summary ────────────────────────────────────────
    print()
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ PASSED : {passed}/{len(test_cases)}")
    print(f"❌ FAILED : {failed}/{len(test_cases)}")
    print(f"⚠️  ERRORS : {errors}/{len(test_cases)}")
    print(f"📈 SCORE  : {round(passed/len(test_cases)*100)}%")
    print(f"📄 Results saved to: {filename}")
    print("=" * 60)

    # ── Print Failed Questions ───────────────────────────────
    failed_tests = [r for r in results if "FAIL" in r["result"]]
    if failed_tests:
        print()
        print("❌ FAILED QUESTIONS:")
        for r in failed_tests:
            print(f"  [{r['country']}] {r['question']}")
            print(f"  Expected keywords: {r['expected_keywords']}")
            print()


if __name__ == "__main__":
    main()
