Autor:
Maciej Dobrowolski nr indeksu 320 678

Cel i opis projektu:
Celem projektu było stworzenie gry podobnej do Angry Birds. Gracz ma za zadanie ustawić kursorem myszy kąt oraz siłę wystrzelenia pocisku i zestrzelić wszystkie cele, które ukrywają się za osłonami. Po zestrzeleniu wszystkich przeciwników gracz przechodzi do kolejnego poziomu.

Instrukcja uruchomienia:


Opis programu.
Do wykonania programu zostały użyte dwie biblioteki pymunk oraz pygame. Pymunk jest odpowiedzialny za generowanie całej fizyki pod spodem, natomiast zadaniem PyGame jest wyrysowanie całej gry a także pobieranie wejścia od użygkownika.
Program składa się z następujących klas:
- Bird
- Enemy
- Obstacle
- Level
- Game

Klasa Bird zawiera zawiera infromacje o każdym z ptaku znajdującym się aktualnie na ekranie. Zawiera informacje takie jak