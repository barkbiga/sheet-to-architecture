
## 1. Installation

Python ≥ 3.9 :

```bash
python3 -m venv .venvdiag
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install pandas jinja2 openpyxl plantuml python-pptx
```

## 2. Lancer la génération

```bash
python3 generate_presentation.py \
    -i petstore_archi_v3.xlsx \
    -o docs_single/presentation.pptx

python3 build_docs.py -i petstore_archi.xlsx       # produit /docs


# 1. Diagrammes
python3 generate_diagrams.py -i petstore_archi_v3.xlsx -o diagrams

# 2. Docs multi-audiences
python3 build_docs_multi.py -i petstore_archi_v3.xlsx
# → docs_multi/{architecture.md, executive.md, runbook.md} (+ diagrams)

# 3. Slides exécutives (optionnel)
python3 generate_slides_exec.py -i petstore_archi_v3.xlsx -d diagrams -o executive_deck.pptx

#4. Executer le main avec les diagrammes et docs
python3 main.py -i petstore_archi_v3.xlsx
```


# Execution dans docker
Le script Python utilisant `pandas` dans un conteneur Docker, afin d’éviter les problèmes d’antivirus (ex. : McAfee) et garantir un environnement cohérent.

```bash
docker build -t sheet-to-architecture .

# Windows
docker run --rm -v %cd%:/app sheet-to-architecture

# Linux / WSL
docker run --rm -v $(pwd):/app sheet-to-architecture

# Exemple : monter un dossier contenant des fichiers Excel
docker run --rm -v %cd%:/app -v C:\chemin\vers\excels:/data sheet-to-architecture

docker rmi sheet-to-architecture
```