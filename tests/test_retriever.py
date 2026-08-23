from app.rag.retriever import ParcelPilotRetriever


retriever = ParcelPilotRetriever()


print("\n================================")
print("TEST 1: NORTHSTAR CANCELLATION")
print("================================")

results = retriever.search(
    "Can Northstar cancel a BOOKED shipment without a cancellation fee?",
    account_id="ACCT-001"
)

for i, result in enumerate(results, 1):

    print(f"\n--- RESULT {i} ---")

    print("Source:")
    print(result["metadata"].get("source", "Unknown"))

    print("Status:")
    print(result["metadata"].get("status", "Unknown"))

    print("Account:")
    print(result["metadata"].get("account_id", "GLOBAL"))

    print("Content:")
    print(result["content"])

    print("Distance:")
    print(result["distance"])