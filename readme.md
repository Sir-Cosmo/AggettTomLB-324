# LB 324

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
## Aufgabe 4
Erklären Sie hier, wie Sie das Passwort aus Ihrer lokalen `.env` auf Azure übertragen.
