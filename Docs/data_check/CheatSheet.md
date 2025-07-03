# Cheat Sheet: Data Check

## Essenz
Die Data-Check-Komponente stellt die Qualität und Integrität der eingehenden Daten für die ML-Pipeline sicher. Sie verwendet `pytest`, um verschiedene Aspekte der Daten zu validieren, von Spaltennamen bis hin zu Verteilungsähnlichkeiten, und identifiziert potenzielle Datenprobleme frühzeitig.

## Verwendete Funktionen (test_data.py)

*   `test_column_names`: Überprüft die Spaltennamen und deren Reihenfolge.
*   `test_neighborhood_names`: Überprüft die Gültigkeit der Nachbarschaftsnamen.
*   `test_proper_boundaries`: Überprüft die geografischen Grenzen von Längen- und Breitengraden.
*   `test_similar_neigh_distrib`: Misst die Ähnlichkeit der Nachbarschaftsverteilung mittels KL-Divergenz.
*   `test_row_count`: Überprüft die Anzahl der Zeilen im Datensatz.
*   `test_price_range`: Überprüft, ob die Preise innerhalb eines gültigen Bereichs liegen.