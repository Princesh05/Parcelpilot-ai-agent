from pathlib import Path


DOCUMENT_METADATA = {

    "01_Support_Policy_v3_CURRENT.pdf": {
        "document_type": "support_policy",
        "status": "CURRENT",
        "scope": "global",
        "account_id": "GLOBAL",
        "authority": 90,
        "effective_date": "2026-05-01",
    },

    "02_Support_Policy_v2_DEPRECATED.pdf": {
        "document_type": "support_policy",
        "status": "DEPRECATED",
        "scope": "global",
        "account_id": "GLOBAL",
        "authority": 10,
        "effective_date": "2025-01-01",
    },

    "03_Cancellation_and_Service_Credit_SOP_v4.pdf": {
        "document_type": "sop",
        "status": "CURRENT",
        "scope": "global",
        "account_id": "GLOBAL",
        "authority": 95,
        "effective_date": "2026-06-15",
    },

    "04_Product_Operations_Guide_and_Known_Issues.pdf": {
        "document_type": "product_documentation",
        "status": "CURRENT",
        "scope": "global",
        "account_id": "GLOBAL",
        "authority": 90,
        "effective_date": "2026-08-14",
    },

    "05_Northstar_Logistics_Enterprise_Agreement.pdf": {
        "document_type": "customer_agreement",
        "status": "ACTIVE",
        "scope": "account",
        "account_id": "ACCT-001",
        "authority": 100,
        "effective_date": "2026-01-01",
    },

    "06_LumenWorks_Service_Agreement.pdf": {
        "document_type": "customer_agreement",
        "status": "ACTIVE",
        "scope": "account",
        "account_id": "ACCT-002",
        "authority": 100,
        "effective_date": "2026-03-01",
    },
}


def get_document_metadata(filename):

    filename = Path(filename).name

    return DOCUMENT_METADATA.get(
        filename,
        {
            "document_type": "unknown",
            "status": "UNKNOWN",
            "scope": "unknown",
            "account_id": "UNKNOWN",
            "authority": 0,
            "effective_date": "UNKNOWN",
        }
    )