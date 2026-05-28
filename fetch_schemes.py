import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='SchemeRAG/1.0'
)

schemes = {
    "pm_kisan": "Pradhan Mantri Kisan Samman Nidhi",
    "ayushman_bharat": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana",
    "mgnrega": "Mahatma Gandhi National Rural Employment Guarantee Act",
    "pm_awas_yojana": "Pradhan Mantri Awas Yojana",
    "atal_pension": "Atal Pension Yojana"
}

import os
os.makedirs("scheme_rag/data", exist_ok=True)

for filename, title in schemes.items():
    page = wiki.page(title)
    if page.exists():
        with open(f"scheme_rag/data/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(page.text)
        print(f"✓ Saved {filename}.txt — {len(page.text)} characters")
    else:
        print(f"✗ NOT FOUND: {title}")