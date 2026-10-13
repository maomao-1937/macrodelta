"""Local sentence embeddings; first use downloads an Apache-2.0 model."""


class LocalEmbedder:
    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def similarities(self, queries: list[str], documents: list[str]) -> list[list[float]]:
        from sentence_transformers import util

        query_vectors = self.model.encode(queries, convert_to_tensor=True, normalize_embeddings=True)
        document_vectors = self.model.encode(documents, convert_to_tensor=True, normalize_embeddings=True)
        return util.cos_sim(query_vectors, document_vectors).tolist()
