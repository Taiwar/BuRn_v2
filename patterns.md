# Suchmuster Notizen

## Cheatsheet

- Spaces/Tabs/usw.: `\s`
- Buchstaben/Zahlen: `\w`
- Beliebiger char: `.`
- 1 oder mehr: `+`
- Char-Gruppe: `[]`

## Praktische Suchmuster

- Alle Klammern und was darin steht: `\([\w\s]+\)` bzw. `\[[\w\s]+\]`
- Alles nach einem Bindestrich und einer Leerzeile davor: `\s-[\w\s]+`

## Zum Ausprobieren
https://regexr.com