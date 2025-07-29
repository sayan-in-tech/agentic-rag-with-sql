import sqlite3
import json
from typing import List, Dict


def get_all_tables(conn) -> List[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    return tables


def get_table_schema(conn, table: str) -> Dict:
    cursor = conn.cursor()

    # Columns and types
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()  # Each: (cid, name, type, notnull, dflt_value, pk)

    column_data = []
    for col in columns:
        column_data.append({
            "name": col[1],
            "type": col[2],
            "primary_key": bool(col[5]),
            "not_null": bool(col[3])
        })

    # Foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table});")
    foreign_keys = cursor.fetchall()
    fk_data = []
    for fk in foreign_keys:
        fk_data.append({
            "column": fk[3],
            "ref_table": fk[2],
            "ref_column": fk[4]
        })

    return {
        "table": table,
        "columns": column_data,
        "foreign_keys": fk_data
    }


def format_schema_chunk(table_schema: Dict) -> str:
    lines = [f"Table: {table_schema['table']}"]

    lines.append("Columns:")
    for col in table_schema['columns']:
        line = f"  - {col['name']} ({col['type']})"
        if col["primary_key"]:
            line += " [PK]"
        if col["not_null"]:
            line += " [NOT NULL]"
        lines.append(line)

    if table_schema['foreign_keys']:
        lines.append("Foreign Keys:")
        for fk in table_schema['foreign_keys']:
            lines.append(f"  - {fk['column']} → {fk['ref_table']}.{fk['ref_column']}")

    return "\n".join(lines)


def extract_all_schema_chunks(db_path: str) -> List[str]:
    conn = sqlite3.connect(db_path)
    tables = get_all_tables(conn)

    chunks = []
    for table in tables:
        schema = get_table_schema(conn, table)
        chunk = format_schema_chunk(schema)
        chunks.append(chunk)

    conn.close()
    return chunks


def save_chunks_to_json(chunks: List[str], output_path: str):
    with open(output_path, "w") as f:
        json.dump(chunks, f, indent=2)


if __name__ == "__main__":
    db_path = "persistence\db\Chinook_Sqlite.db"  # Update if your DB is named differently
    output_json = "RAG\chinook_schema_chunks.json"

    chunks = extract_all_schema_chunks(db_path)
    save_chunks_to_json(chunks, output_json)

    print(f"✅ Extracted {len(chunks)} schema chunks.")
    print(f"📄 Saved to {output_json}")
