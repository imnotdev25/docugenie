import numpy as np
from sqlmodel import select
from app.databases.db import get_session
from app.models.embeddings import TextEmbedding
from app.logger import logger


def save_embeddings(index_name: str, doc_metadata: dict, embeddings: list, doc_uuid: str):
    with next(get_session()) as session:
        try:
            converted_embeddings = [np.array(emb, dtype=np.float32).tolist() for emb in embeddings]
            logger.info(f"Saving {len(converted_embeddings)} embeddings to index {index_name}")
            logger.info(f"Length of each embedding: {len(converted_embeddings[0])}")

            for embedding in converted_embeddings:
                new_entry = TextEmbedding(
                    index_name=index_name,
                    doc_metadata=doc_metadata,
                    embedding=embedding,
                    doc_uuid=doc_uuid
                )
                session.add(new_entry)

            session.commit()
        except Exception as err:
            logger.error(f"Error saving embeddings: {err}")
            raise Exception(f"Error saving embeddings: {err}") from err


def query_similar_embeddings(query_embedding: str, top_n: int = 5):
    query_vector = np.array(query_embedding, dtype=np.float32).tolist()

    with next(get_session()) as session:
        stmt = select(TextEmbedding).order_by(
            TextEmbedding.embedding.l2_distance(query_vector)
        ).limit(top_n)

        results = session.exec(stmt).all()
        logger.info(f"Found {len(results)} similar embeddings")
        return results