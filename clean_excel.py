"""
clean_excel.py
--------------
Run this script once to clean your MTDR Excel and index it into ChromaDB.
Usage: python clean_excel.py --file "MTDR Records.xlsx"
"""

import argparse
import re
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# ── Config ──────────────────────────────────────────────────────────────────
COLLECTION_NAME = "mtdr_records"
DB_PATH = "./chroma_db"          # folder where ChromaDB stores data
EMBED_MODEL = "all-MiniLM-L6-v2" # small, fast, runs fully offline

# Column name aliases — edit these to match your actual Excel column headers
COL_MACHINE  = ["machine", "machine name", "equipment", "asset"]
COL_PROBLEM  = ["problem", "issue", "fault", "description", "breakdown"]
COL_SOLUTION = ["solution", "action taken", "fix", "resolution", "remedy"]


def find_col(df_cols, aliases):
    """Return the first column name from df that matches any alias (case-insensitive)."""
    lower_cols = {c.lower().strip(): c for c in df_cols}
    for alias in aliases:
        if alias in lower_cols:
            return lower_cols[alias]
    return None


def clean_text(val):
    if pd.isna(val):
        return ""
    text = str(val).strip()
    text = re.sub(r"\s+", " ", text)          # collapse whitespace
    text = re.sub(r"[^\x20-\x7E\u0900-\u097F]", "", text)  # strip non-printable
    return text.strip()


def load_and_clean(filepath: str) -> pd.DataFrame:
    print(f"[1/3] Reading: {filepath}")
    df = pd.read_excel(filepath, engine="openpyxl")

    # Normalise column names for matching
    df.columns = df.columns.str.strip()

    machine_col  = find_col(df.columns, COL_MACHINE)
    problem_col  = find_col(df.columns, COL_PROBLEM)
    solution_col = find_col(df.columns, COL_SOLUTION)

    missing = []
    if not machine_col:  missing.append("Machine")
    if not problem_col:  missing.append("Problem")
    if not solution_col: missing.append("Solution")
    if missing:
        raise ValueError(
            f"Could not find columns for: {missing}.\n"
            f"Available columns: {list(df.columns)}\n"
            f"Edit COL_MACHINE / COL_PROBLEM / COL_SOLUTION aliases in this script."
        )

    print(f"   Mapped → Machine='{machine_col}', Problem='{problem_col}', Solution='{solution_col}'")

    cleaned = pd.DataFrame({
        "machine":  df[machine_col].apply(clean_text),
        "problem":  df[problem_col].apply(clean_text),
        "solution": df[solution_col].apply(clean_text),
    })

    before = len(cleaned)
    cleaned = cleaned[
        (cleaned["problem"].str.len() > 5) &
        (cleaned["solution"].str.len() > 5)
    ].drop_duplicates(subset=["machine", "problem", "solution"])
    print(f"   Rows: {before} → {len(cleaned)} after cleaning")
    return cleaned.reset_index(drop=True)


def index_to_chromadb(df: pd.DataFrame):
    print(f"[2/3] Connecting to ChromaDB at '{DB_PATH}'")
    client = chromadb.PersistentClient(path=DB_PATH)

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    # Delete old collection to rebuild fresh
    try:
        client.delete_collection(COLLECTION_NAME)
        print("   Deleted existing collection (rebuilding fresh)")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    # Build documents: combine machine + problem for better retrieval
    documents = []
    metadatas = []
    ids = []

    for i, row in df.iterrows():
        doc = f"Machine: {row['machine']}. Problem: {row['problem']}"
        documents.append(doc)
        metadatas.append({
            "machine":  row["machine"],
            "problem":  row["problem"],
            "solution": row["solution"],
        })
        ids.append(f"rec_{i}")

    # Batch insert (ChromaDB recommends ≤ 500 at a time)
    batch = 500
    for start in range(0, len(documents), batch):
        collection.add(
            documents=documents[start:start+batch],
            metadatas=metadatas[start:start+batch],
            ids=ids[start:start+batch],
        )
        print(f"   Indexed {min(start+batch, len(documents))}/{len(documents)} records")

    print(f"[3/3] Done. {len(documents)} records indexed.")


def main():
    parser = argparse.ArgumentParser(description="Clean MTDR Excel and index into ChromaDB")
    parser.add_argument("--file", required=True, help="Path to your MTDR Excel file")
    args = parser.parse_args()

    df = load_and_clean(args.file)
    index_to_chromadb(df)
    print("\nAll done! Now start the server with: uvicorn app:app --host 127.0.0.1 --port 8000")


if __name__ == "__main__":
    main()
