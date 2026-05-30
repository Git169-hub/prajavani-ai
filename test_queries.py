import time
from rag_engine import answer_query

test_cases = [
    # PM Kisan - English
    ("What is PM Kisan scheme?", "pm_kisan"),
    ("Who is eligible for PM Kisan?", "pm_kisan"),
    ("How much money does PM Kisan give per year?", "pm_kisan"),
    ("How to apply for PM Kisan?", "pm_kisan"),

    # PM Kisan - Telugu
    ("పీఎం కిసాన్ పథకం అంటే ఏమిటి?", "pm_kisan_telugu"),
    ("పీఎం కిసాన్ కి అర్హత ఏమిటి?", "pm_kisan_telugu"),
    ("పీఎం కిసాన్ లో ఎంత డబ్బు వస్తుంది?", "pm_kisan_telugu"),

    # Ayushman Bharat - English
    ("What is Ayushman Bharat scheme?", "ayushman_bharat"),
    ("How much health cover does Ayushman Bharat give?", "ayushman_bharat"),
    ("Who is eligible for Ayushman Bharat?", "ayushman_bharat"),

    # Ayushman Bharat - Telugu
    ("ఆయుష్మాన్ భారత్ అర్హత ఏమిటి?", "ayushman_bharat_telugu"),
    ("ఆయుష్మాన్ భారత్ లో ఎంత బీమా వస్తుంది?", "ayushman_bharat_telugu"),

    # MGNREGA - English
    ("What is MGNREGA scheme?", "mgnrega"),
    ("How many days of work does MGNREGA guarantee?", "mgnrega"),

    # MGNREGA - Telugu
    ("MGNREGA లో ఎన్ని రోజులు పని హామీ ఇస్తారు?", "mgnrega_telugu"),
    ("MGNREGA కి దరఖాస్తు ఎలా చేయాలి?", "mgnrega_telugu"),

    # PM Awas Yojana - English
    ("What is PM Awas Yojana?", "pm_awas_yojana"),
    ("How to apply for PM Awas Yojana?", "pm_awas_yojana"),

    # Atal Pension - English
    ("What is Atal Pension Yojana?", "atal_pension"),

    # Atal Pension - Telugu
    ("అటల్ పెన్షన్ యోజన వయసు పరిమితి ఏమిటి?", "atal_pension_telugu"),
]

passed = 0
failed = 0
failures = []

for query, expected_source in test_cases:
    result = answer_query(query)
    time.sleep(3) 
    answer = result["answer"]
    sources = result["sources"]

    hit = any(expected_source in s for s in sources)
    if hit:
        passed += 1
        print(f"✅ PASS | {query[:50]}")
    else:
        failed += 1
        failures.append((query, expected_source, sources))
        print(f"❌ FAIL | {query[:50]}")
        print(f"   Expected: {expected_source} | Got: {sources}")

print(f"\n--- RESULTS ---")
print(f"Passed: {passed}/20")
print(f"Failed: {failed}/20")
print(f"Accuracy: {round(passed/20*100)}%")