"""
Test LLM Service independently before integration

Run: python test_llm.py
"""

from app.services.llm.groq_llm_service import (
    GroqLLMService
)

service = GroqLLMService()

# Test 1: Aadhaar extraction
print("=" * 50)
print("TEST 1: Aadhaar Extraction")
print("=" * 50)

text_aadhaar = """
Government of India
Unique Identification Authority of India

Name: Rahul Sharma
Date of Birth: 12/05/1998
Aadhaar Number: 1234 5678 9012
"""

result = service.extract_fields(
    text=text_aadhaar,
    fields=[
        "name",
        "dob",
        "aadhaar_number"
    ]
)

print("Extracted:")
print(result)
print()

# Test 2: Passport extraction
print("=" * 50)
print("TEST 2: Passport Extraction")
print("=" * 50)

text_passport = """
Republic of India
PASSPORT

Passport Number: A1234567
Nationality: Indian
"""

result = service.extract_fields(
    text=text_passport,
    fields=[
        "passport_number",
        "nationality"
    ]
)

print("Extracted:")
print(result)
print()

# Test 3: Invoice extraction
print("=" * 50)
print("TEST 3: Invoice Extraction")
print("=" * 50)

text_invoice = """
INVOICE

Invoice Number: INV-2024-001
Date: 2024-05-08
Total Amount: 15000.00
"""

result = service.extract_fields(
    text=text_invoice,
    fields=[
        "invoice_number",
        "total_amount"
    ]
)

print("Extracted:")
print(result)
print()

print("=" * 50)
print("All tests completed!")
print("=" * 50)
