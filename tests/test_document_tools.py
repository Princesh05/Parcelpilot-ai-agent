from app.tools.document_tools import search_documents


northstar_user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}


lumenworks_user = {
    "user_id": "user_002",
    "role": "customer",
    "account_id": "ACCT-002"
}


print("\n================================")
print("NORTHSTAR DOCUMENT SEARCH")
print("================================")


result = search_documents(
    query="Can I cancel a BOOKED shipment without a cancellation fee?",
    user_context=northstar_user
)


for item in result["results"]:

    print("\n----------------------------")

    print("Source:", item["source"])

    print("Account:", item["account_id"])

    print("Status:", item["status"])

    print("Authority:", item["authority"])

    print("Content:")
    print(item["content"])


print("\n================================")
print("LUMENWORKS DOCUMENT SEARCH")
print("================================")


result = search_documents(
    query="Can I cancel a BOOKED shipment without a cancellation fee?",
    user_context=lumenworks_user
)


for item in result["results"]:

    print("\n----------------------------")

    print("Source:", item["source"])

    print("Account:", item["account_id"])

    print("Status:", item["status"])

    print("Authority:", item["authority"])