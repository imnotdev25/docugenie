import numpy as np
from sqlmodel import select, text
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
            logger.info(f"Saved {len(converted_embeddings)} embeddings")
        except Exception as err:
            logger.error(f"Error saving embeddings: {err}")
            raise Exception(f"Error saving embeddings: {err}") from err


def query_similar_embeddings(query_embedding: list, top_n: int = 5):

    with next(get_session()) as session:
        stmt = select(TextEmbedding.embedding).order_by(
            TextEmbedding.embedding.l2(query_embedding)
        ).limit(top_n)

        results = session.exec(stmt).all()
        logger.info(f"Found {len(results)} similar embeddings")
        return results