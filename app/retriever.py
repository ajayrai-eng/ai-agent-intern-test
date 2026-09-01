import re
from sklearn.feature_extraction.text import TfidfVectorizer

from .knowledge import load_knowledge_base


class Retriever:
    def __init__(self):
        self.chunks = load_knowledge_base()

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
        )

        self.matrix = self.vectorizer.fit_transform(
            [c.text for c in self.chunks]
        )

    def authority_bonus(self, chunk):
        m = chunk.metadata
        bonus = 0

        if m.get("status") == "active":
            bonus += 0.30

        if m.get("policy_authority") == "official":
            bonus += 0.30

        if m.get("audience") == "customer":
            bonus += 0.10

        if m.get("status") in {"superseded", "draft"}:
            bonus -= 0.50

        if m.get("audience") == "internal":
            bonus -= 0.40

        return bonus

    def search(self, query, top_k=5):
        q = self.vectorizer.transform([query])

        similarities = (self.matrix @ q.T).toarray().ravel()

        results = []

        for i, chunk in enumerate(self.chunks):
            score = float(similarities[i]) + self.authority_bonus(chunk)

            results.append({
                "score": round(score, 4),
                "filename": chunk.filename,
                "heading": chunk.heading,
                "text": chunk.text,
                "metadata": chunk.metadata,
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]