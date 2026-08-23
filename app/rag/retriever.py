from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "chroma_db"


class ParcelPilotRetriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_collection(
            name="parcelpilot_documents"
        )

    def search(
        self,
        query,
        account_id=None,
        top_k=5
    ):
        """
        Search ParcelPilot documents.

        Global documents are always eligible.

        Account-specific documents are only eligible
        when they belong to the requested account.
        """

        # Get more candidates first.
        results = self.collection.query(
            query_texts=[query],
            n_results=10
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        candidates = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            document_account = metadata.get(
                "account_id",
                "GLOBAL"
            )

            # Global documents can be used.
            if document_account == "GLOBAL":

                candidates.append({
                    "content": document,
                    "metadata": metadata,
                    "distance": distance
                })

            # Account-specific documents can only be
            # used for that account.
            elif (
                account_id is not None
                and document_account == account_id
            ):

                candidates.append({
                    "content": document,
                    "metadata": metadata,
                    "distance": distance
                })

        # Rank documents using both:
        #
        # 1. Semantic relevance
        # 2. Source authority

        def ranking_score(item):

            distance = item["distance"]

            authority = float(
                item["metadata"].get(
                    "authority",
                    0
                )
            )

            authority_score = authority / 100

            relevance_score = 1 / (1 + distance)

            return (
                relevance_score * 0.6
                +
                authority_score * 0.4
            )

        candidates.sort(
            key=ranking_score,
            reverse=True
        )

        return candidates[:top_k]