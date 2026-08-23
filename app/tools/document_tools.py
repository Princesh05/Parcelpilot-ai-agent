from app.rag.retriever import ParcelPilotRetriever


retriever = ParcelPilotRetriever()


def search_documents(
    query,
    user_context,
    top_k=5
):
    """
    Search ParcelPilot documents while respecting
    the user's account access.
    """

    role = user_context.get("role")

    account_id = user_context.get(
        "account_id"
    )

    # Customer users must have an account.
    if role == "customer" and not account_id:

        return {
            "success": False,
            "error": "Customer account context is required."
        }

    results = retriever.search(
        query=query,
        account_id=account_id,
        top_k=top_k
    )

    formatted_results = []

    for result in results:

        metadata = result["metadata"]

        formatted_results.append({
            "content": result["content"],
            "source": metadata.get(
                "source",
                "Unknown"
            ),
            "status": metadata.get(
                "status",
                "UNKNOWN"
            ),
            "scope": metadata.get(
                "scope",
                "unknown"
            ),
            "account_id": metadata.get(
                "account_id",
                "GLOBAL"
            ),
            "authority": metadata.get(
                "authority",
                0
            ),
            "distance": result["distance"]
        })

    return {
        "success": True,
        "results": formatted_results
    }