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

Klasa Bird zawiera zawiera infromacje o każdym z ptaku znajdującym się aktualnie na ekranie. Zawiera informacje takie jak shape i body - elementy niezbędne do generowania fizyki. Body zawiera fizyczne właśniwości objektu, takie jak rotacja, pozycja, prędkość lub masa, a shape definiuje kształt ciała. Tworzony jest obiekt początkowo statyczny (w miejscu wystrzelenia), po strzale ulega zmianie na typ dynamiczny. Pozwala wyrysować obiekt.

Klasa Enemy jest podobnie zbudowana do klasy Bird. Rózni się ona tym, że rozpoczyna już jako obiekt dynamiczny. Zmienia się wartość collision_type, co pozwoli zdefiniować kolizję obiektu tej klasy z innymi. Pozwala wyrysować obiekt.

Klasa Obstacle zawiera wszystkie informacje o przeszkodach zasłaniających przeciwników. Zdefiniowane są dwa typy przeszków: 'beam' i 'column'. Różnią się one startową pozycją, co ułatwia pozycjonowanie elementów w tworzeniu poziomów. Pozwala wyrysować obiekt.

Klasa Game jest odpowiedzialna za przebieg całej gry.