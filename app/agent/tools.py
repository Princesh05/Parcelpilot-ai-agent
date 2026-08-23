from app.tools.data_tools import (
    lookup_account,
    lookup_order,
    lookup_ticket
)

from app.tools.document_tools import (
    search_documents
)

from app.tools.action_tools import (
    prepare_escalation,
    create_escalation,
    prepare_cancellation,
    cancel_order
)


def execute_tool(
    tool_name,
    arguments,
    user_context
):
    """
    Central tool dispatcher.

    The LLM chooses a tool name,
    but Python decides which actual
    function gets executed.
    """

    if tool_name == "lookup_account":

        return lookup_account(
            account_id=arguments["account_id"],
            user_context=user_context
        )

    elif tool_name == "lookup_order":

        return lookup_order(
            order_id=arguments["order_id"],
            user_context=user_context
        )

    elif tool_name == "lookup_ticket":

        return lookup_ticket(
            ticket_id=arguments["ticket_id"],
            user_context=user_context
        )

    elif tool_name == "search_documents":

        return search_documents(
            query=arguments["query"],
            user_context=user_context,
            top_k=arguments.get("top_k", 5)
        )

    elif tool_name == "prepare_cancellation":

        return prepare_cancellation(
            order_id=arguments["order_id"],
            user_context=user_context
        )

    elif tool_name == "cancel_order":

        return cancel_order(
            order_id=arguments["order_id"],
            user_context=user_context,
            confirmed=arguments.get(
                "confirmed",
                False
            )
        )

    elif tool_name == "prepare_escalation":

        return prepare_escalation(
            ticket_id=arguments["ticket_id"],
            reason=arguments["reason"],
            priority=arguments["priority"],
            user_context=user_context
        )

    elif tool_name == "create_escalation":

        return create_escalation(
            ticket_id=arguments["ticket_id"],
            reason=arguments["reason"],
            priority=arguments["priority"],
            user_context=user_context,
            confirmed=arguments.get(
                "confirmed",
                False
            )
        )

    else:

        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }