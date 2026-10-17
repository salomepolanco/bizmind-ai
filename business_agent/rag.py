
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from google import genai
from google.genai import types


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
DB_DIR = BASE_DIR / "chroma_db"


client = genai.Client()

chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma_client.get_or_create_collection(
    name="business_knowledge"
)


def crear_embedding(texto: str) -> list[float]:
    """Convierte un texto en un vector usando embeddings de Gemini."""
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texto,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return response.embeddings[0].values


def indexar_documentos() -> int:
    """Indexa los documentos Markdown de knowledge/ en ChromaDB."""
    documentos = []

    for archivo in KNOWLEDGE_DIR.glob("*.md"):
        contenido = archivo.read_text(encoding="utf-8").strip()

        if contenido:
            documentos.append((archivo.name, contenido))

    if not documentos:
        raise ValueError(
            f"No se encontraron documentos Markdown en {KNOWLEDGE_DIR}"
        )

    ids = [nombre for nombre, _ in documentos]
    textos = [contenido for _, contenido in documentos]
    embeddings = [crear_embedding(texto) for texto in textos]

    collection.upsert(
        ids=ids,
        documents=textos,
        embeddings=embeddings,
        metadatas=[{"archivo": nombre} for nombre in ids],
    )

    return len(documentos)


def buscar_conocimiento(pregunta: str, cantidad: int = 2) -> str:
    """Recupera los documentos más relevantes para una pregunta."""
    if collection.count() == 0:
        indexar_documentos()

    embedding = crear_embedding(pregunta)

    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=min(cantidad, collection.count()),
    )

    documentos = resultados.get("documents", [[]])[0]

    if not documentos:
        return "No se encontró información relevante en la base de conocimiento."

    return "\n\n".join(documentos)
