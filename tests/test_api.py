from fastapi.testclient import TestClient

from app.api.routes import app


client = TestClient(app)


print("\n========================================")
print("       PARCELPILOT API TESTS")
print("========================================")


# ========================================
# TEST 1: HEALTH CHECK
# ========================================

print("\n================================")
print("TEST 1: HEALTH CHECK")
print("================================")

response = client.get("/health")

print("STATUS:", response.status_code)
print("RESULT:", response.json())

assert response.status_code == 200
assert response.json()["status"] == "healthy"

print("✅ Health check passed")


# ========================================
# TEST 2: INVALID REQUEST
# ========================================

print("\n================================")
print("TEST 2: INVALID REQUEST")
print("================================")

response = client.post(
    "/chat",
    json={
        "user_context": {
            "user_id": "user_001",
            "account_id": "ACCT-001",
            "role": "customer"
        }
    }
)

print("STATUS:", response.status_code)
print("RESULT:", response.json())

assert response.status_code == 422

print("✅ Validation correctly rejected invalid request")


# ========================================
# TEST 3: VALID REQUEST STRUCTURE
# ========================================

print("\n================================")
print("TEST 3: VALID CHAT REQUEST")
print("================================")

response = client.post(
    "/chat",
    json={
        "message": "What is the status of my order?",
        "user_context": {
            "user_id": "user_001",
            "account_id": "ACCT-001",
            "role": "customer"
        }
    }
)

print("STATUS:", response.status_code)
print("RESULT:", response.json())

assert response.status_code == 200

print("✅ Chat endpoint accepted valid request")


print("\n========================================")
print("🎉 API TESTS COMPLETED")
print("========================================")