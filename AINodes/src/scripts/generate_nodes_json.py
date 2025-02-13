import os
import json
import re

# Basisverzeichnis, wo deine Nodes gespeichert sind
BASE_PACKAGE = "AINodes.src.nodes"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "nodes"))

# Neuer Speicherort für nodes.json
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
NODES_JSON_PATH = os.path.join(DATA_DIR, "nodes.json")

def find_nodes():
    """Sucht automatisch nach allen Nodes und speichert sie in einer JSON-Datei."""
    if not os.path.exists(BASE_DIR):
        raise FileNotFoundError(f"❌ Fehler: Der Nodes-Ordner wurde nicht gefunden: {BASE_DIR}")

    print(f"🔍 Scanne Nodes in: {BASE_DIR}")

    nodes = {}

    # Rekursiv alle Python-Dateien in Unterordnern durchsuchen
    for root, _, files in os.walk(BASE_DIR):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                module_path = os.path.relpath(os.path.join(root, filename), BASE_DIR)  # Relativer Pfad
                module_name = module_path.replace(os.sep, ".")[:-3]  # Ersetze / durch . und entferne ".py"

                full_module_path = f"{BASE_PACKAGE}.{module_name}"  # Kompletter Import-Pfad

                print(f"📂 Gefundene Datei: {filename} -> {full_module_path}")  # Debugging

                # Versuche die Datei zu öffnen und nach Node-Klassen zu suchen
                with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"class (\w+)\(", line)
                        if match:
                            class_name = match.group(1)  # Klassennamen extrahieren
                            nodes[class_name] = f"{full_module_path}.{class_name}"
                            print(f"✅ Node gefunden: {class_name} -> {full_module_path}")  # Debugging

    # Stelle sicher, dass der Ordner existiert
    os.makedirs(DATA_DIR, exist_ok=True)

    # Speichere die gefundenen Nodes als JSON
    with open(NODES_JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(nodes, json_file, indent=4)

    print(f"✅ {len(nodes)} Nodes gefunden und in {NODES_JSON_PATH} gespeichert!")

if __name__ == "__main__":
    find_nodes()
