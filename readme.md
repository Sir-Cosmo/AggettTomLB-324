# LB 324

# Tagebuch-App — CI/CD (Render)

**Live URL:** [https://aggetttomlb-324.onrender.com](https://aggetttomlb-324.onrender.com/)

## Branch-Konzept
- main: stets produktionsgleich; jeder Merge triggert eine Auslieferung (Render Deploy Hook)
- dev: stabil getesteter Code; PRs von feature/* nach dev
- feature/*: Entwicklungs-Äste pro Feature

## pre-commit verwenden
```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push



## Aufgabe 2
Erklären Sie hier, wie man `pre-commit` installiert.

## pre-commit verwenden

Installieren und Hooks aktivieren:
```bash
pip install pre-commit
pre-commit install                  # aktiviert commit-Hooks (Black, Ruff, isort)
pre-commit install --hook-type pre-push   # aktiviert push-Hook (pytest)
```
Hooks manuell ausführen:
```
pre-commit run --all-files   # format/lint über alle Dateien
pytest -q                    # Tests lokal starten
```


**Goal:** Every PR targeting `dev` runs tests, nothing else.

Create file **`.github/workflows/pr-tests.yml`**:

```yaml
name: PR tests (to dev)

on:
  pull_request:
    branches: [ "dev" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
```



## Aufgabe 4
Erklären Sie hier, wie Sie das Passwort aus Ihrer lokalen `.env` auf Azure übertragen.
