from pathlib import Path

def read_file(path):

    path = Path(path)

    if not path.exists():
        return "ERROR: archivo no encontrado"

    try:

        with open(path, "r", encoding="utf-8", errors="ignore") as f:

            content = f.read()

        return content[:15000]

    except Exception as e:

        return f"ERROR: {str(e)}"
