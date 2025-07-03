# Detaillierte Erklärungen: Data Check

## Hintergrund
Der Data Check ist eine entscheidende Komponente in einer Machine Learning (ML)-Pipeline. Sein Hauptzweck ist es, die Qualität und Integrität der eingehenden Daten sicherzustellen. Dies beinhaltet die Erkennung von Datenabweichungen, Inkonsistenzen oder Anomalien, die die Leistung nachfolgender ML-Modelle beeinträchtigen könnten. Durch frühzeitige Überprüfung der Daten wird sichergestellt, dass nur valide und erwartungsgemäße Daten in den Trainings- und Inferenzprozess gelangen.

## Verwendete Methoden

### Pytest
`pytest` ist ein leistungsstarkes und flexibles Test-Framework für Python. Es wird hier verwendet, um automatisierte Tests für die Datenqualität durchzuführen. Die Vorteile von `pytest` in diesem Kontext sind:
*   **Einfache Testschreibung:** Tests können als einfache Funktionen geschrieben werden, die mit `test_` beginnen.
*   **Fixtures:** `pytest` Fixtures (wie in `conftest.py` definiert) ermöglichen die Wiederverwendung von Setup-Code. Sie stellen Testfunktionen benötigte Ressourcen (z.B. geladene DataFrames oder Konfigurationsparameter) zur Verfügung, ohne dass dieser Code in jeder Testfunktion dupliziert werden muss. Dies fördert sauberen und modularen Testcode.
*   **Assertions:** Standard-Python-`assert`-Anweisungen werden verwendet, um Bedingungen zu überprüfen. Wenn eine Assertion fehlschlägt, wird der Test als fehlgeschlagen markiert.

### Wandb Artifacts
`wandb.use_artifact` wird verwendet, um Daten versioniert in die Tests zu laden. Weights & Biases (W&B) Artifacts bieten eine Möglichkeit, Datensätze, Modelle und andere Dateien zu versionieren und zu verfolgen. Durch die Verwendung von `wandb.use_artifact` in den Fixtures (`data` und `ref_data` in `conftest.py`) wird sichergestellt, dass die Tests immer mit der spezifischen Version der Daten ausgeführt werden, die im MLflow-Run angegeben ist. Dies verbessert die Reproduzierbarkeit und Nachvollziehbarkeit der Testergebnisse.

### KL-Divergenz
Die Kullback-Leibler (KL)-Divergenz ist ein Maß dafür, wie stark sich eine Wahrscheinlichkeitsverteilung von einer anderen unterscheidet. Sie wird in der Funktion `test_similar_neigh_distrib` verwendet, um zu beurteilen, ob die Verteilung der `neighbourhood_group`-Spalte in den neuen Daten signifikant von der Verteilung in einem Referenzdatensatz abweicht. Ein hoher KL-Divergenzwert deutet auf eine große Diskrepanz zwischen den Verteilungen hin, was auf eine potenzielle Datenverschiebung oder ein Problem mit den eingehenden Daten hindeuten könnte. Der Test schlägt fehl, wenn die gemessene KL-Divergenz einen vordefinierten Schwellenwert überschreitet.

## Funktionsanalyse (test_data.py)

*   **`test_column_names(data: pd.DataFrame)`**:
    Diese Funktion überprüft, ob der übergebene DataFrame (`data`) alle erwarteten Spaltennamen in der korrekten Reihenfolge enthält. Sie vergleicht die tatsächlichen Spalten des DataFrames mit einer vordefinierten Liste von erwarteten Spalten. Dies stellt sicher, dass das Datenschema konsistent bleibt.

*   **`test_neighborhood_names(data: pd.DataFrame)`**:
    Diese Funktion stellt sicher, dass die Spalte `neighbourhood_group` im DataFrame nur bekannte und gültige Nachbarschaftsnamen enthält. Sie vergleicht die eindeutigen Werte in dieser Spalte mit einer Liste von akzeptierten Namen (z.B. "Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"). Dies hilft, Tippfehler oder unerwartete Kategorien in den Daten zu identifizieren.

*   **`test_proper_boundaries(data: pd.DataFrame)`**:
    Diese Funktion überprüft die geografischen Längen- und Breitengradgrenzen für Immobilien in und um New York City. Sie stellt sicher, dass alle Einträge innerhalb eines plausiblen geografischen Bereichs liegen, um Ausreißer oder fehlerhafte Geodaten zu erkennen.

*   **`test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float)`**:
    Diese Funktion ist entscheidend für die Erkennung von Datenverteilungsänderungen. Sie berechnet die Kullback-Leibler-Divergenz zwischen der Verteilung der `neighbourhood_group`-Spalte in den neuen Daten (`data`) und einem Referenzdatensatz (`ref_data`). Wenn die Divergenz einen bestimmten `kl_threshold` überschreitet, deutet dies auf eine signifikante Verschiebung in der Verteilung hin, was ein Warnsignal für Datenqualitätsprobleme sein kann.

*   **`test_row_count(data: pd.DataFrame)`**:
    Diese Funktion überprüft, ob die Anzahl der Zeilen im DataFrame innerhalb eines erwarteten Bereichs liegt (z.B. zwischen 15.000 und 1.000.000). Dies hilft, leere oder ungewöhnlich große/kleine Datensätze zu identifizieren, die auf Probleme beim Datenladen oder der Datenquelle hindeuten könnten.

*   **`test_price_range(data: pd.DataFrame, min_price: float, max_price: float)`**:
    Diese Funktion stellt sicher, dass alle Preise in der `price`-Spalte des DataFrames innerhalb eines angegebenen Minimum- (`min_price`) und Maximumbereichs (`max_price`) liegen. Dies ist wichtig, um unrealistische oder fehlerhafte Preisangaben zu filtern.