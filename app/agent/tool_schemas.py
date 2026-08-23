TOOLS = [

    # ============================================================
    # 1. LOOKUP ACCOUNT
    # ============================================================

    {
        "name": "lookup_account",
        "description": (
            "Look up a ParcelPilot customer account. "
            "Use this when account information is needed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot account ID, for example ACCT-001."
                    )
                }
            },
            "required": [
                "account_id"
            ]
        }
    },

    # ============================================================
    # 2. LOOKUP ORDER
    # ============================================================

    {
        "name": "lookup_order",
        "description": (
            "Look up shipment/order information such as "
            "status, carrier, booking time, pickup timing, "
            "shipment fee, and fault information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot order ID, for example ORD-1001."
                    )
                }
            },
            "required": [
                "order_id"
            ]
        }
    },

    # ============================================================
    # 3. LOOKUP TICKET
    # ============================================================

    {
        "name": "lookup_ticket",
        "description": (
            "Look up a ParcelPilot support ticket including "
            "status, description, assigned agent, and account."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot ticket ID, for example TKT-504."
                    )
                }
            },
            "required": [
                "ticket_id"
            ]
        }
    },

    # ============================================================
    # 4. SEARCH DOCUMENTS
    # ============================================================

    {
        "name": "search_documents",
        "description": (
            "Search current ParcelPilot policies, customer "
            "agreements, SOPs, product documentation, and "
            "known issues. Use this when answering questions "
            "that depend on policy or documentation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The information to search for."
                    )
                },
                "top_k": {
                    "type": "integer",
                    "description": (
                        "Maximum number of results to return."
                    ),
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": [
                "query"
            ]
        }
    },

    # ============================================================
    # 5. PREPARE CANCELLATION
    # ============================================================

    {
        "name": "prepare_cancellation",
        "description": (
            "Prepare an order cancellation. "
            "This does not cancel the order. "
            "Use this before asking the user for confirmation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot order ID, for example ORD-1001."
                    )
                }
            },
            "required": [
                "order_id"
            ]
        }
    },

    # ============================================================
    # 6. CANCEL ORDER
    # ============================================================

    {
        "name": "cancel_order",
        "description": (
            "Cancel a ParcelPilot order. "
            "This is a state-changing action and must only "
            "be called after explicit user confirmation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot order ID, for example ORD-1001."
                    )
                },
                "confirmed": {
                    "type": "boolean",
                    "description": (
                        "Must be true only when the user "
                        "explicitly confirmed the cancellation."
                    )
                }
            },
            "required": [
                "order_id",
                "confirmed"
            ]
        }
    },

    # ============================================================
    # 7. PREPARE ESCALATION
    # ============================================================

    {
        "name": "prepare_escalation",
        "description": (
            "Prepare an escalation for a support ticket. "
            "This does not create the escalation. "
            "The user must explicitly confirm before creation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot support ticket ID."
                    )
                },
                "reason": {
                    "type": "string",
                    "description": (
                        "Reason why the ticket should be escalated."
                    )
                },
                "priority": {
                    "type": "string",
                    "enum": [
                        "P1",
                        "P2",
                        "P3"
                    ],
                    "description": (
                        "Escalation priority."
                    )
                }
            },
            "required": [
                "ticket_id",
                "reason",
                "priority"
            ]
        }
    },

    # ============================================================
    # 8. CREATE ESCALATION
    # ============================================================

    {
        "name": "create_escalation",
        "description": (
            "Create a support escalation. "
            "This is a state-changing action and must only "
            "be called after explicit user confirmation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": (
                        "ParcelPilot support ticket ID."
                    )
                },
                "reason": {
                    "type": "string",
                    "description": (
                        "Reason why the ticket should be escalated."
                    )
                },
                "priority": {
                    "type": "string",
                    "enum": [
                        "P1",
                        "P2",
                        "P3"
                    ],
                    "description": (
                        "Escalation priority."
                    )
                },
                "confirmed": {
                    "type": "boolean",
                    "description": (
                        "Must be true only when the user "
                        "explicitly confirmed the escalation."
                    )
                }
            },
            "required": [
                "ticket_id",
                "reason",
                "priority",
                "confirmed"
            ]
        }
    }
]