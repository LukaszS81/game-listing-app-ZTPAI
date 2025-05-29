Jak uruchomić projekt?
1. Najpierw trzeba sklonować mój projekt z githuba https://github.com/LukaszS81/game-listing-app-ZTPAI.git
2. Następnie wgrać go na VSC używając git clone https://github.com/LukaszS81/game-listing-app-ZTPAI.git 
3. Gdy już się zgrało projekt wchodzimy do głównego katalogu, a następnie trzeba przejść do backendu(gamesearch) i pobrać plik requirements.txt używając komendy pip install -r requirements.txt
4. Teraz trzeba odpalić dockera, a następnie wpisać docker-compose up --build w VSC
5. Następnie gdy wszystko się już uruchomi trzeba dokonać migracji używając komendy docker-compose exec backend bash następnie python manage.py makemigrations oraz python manage.py migrate
6. Teraz frontend jest dostępny pod adresem http://localhost:3000 backend API pod http://localhost:8000/api/ oraz swagger http://localhost:8000/api/docs/

Użyte technologie:
1. Django REST Framework (DRF)
Umożliwia szybkie budowanie API z gotowym systemem autoryzacji i serializacji danych
2. PostgreSQL
Stabilna i wydajna baza danych SQL, idealna do przechowywania danych o grach i użytkownikach
3. Next.js + Ant Design
Nowoczesny stack frontendowy: Next.js umożliwia SSR (Server Side Rendering), a Ant Design zapewnia szybki start z gotowymi komponentami
4. Docker + Docker Compose
Ułatwia konfigurację środowiska – wystarczy docker-compose up, aby uruchomić całą aplikację (backend, frontend, baza danych, RabbitMQ, Celery)
5. Celery + RabbitMQ
Do obsługi asynchronicznych zadań w tle (np. powiadomień po dodaniu nowej gry)

Funkcjonalności:
1. Rejestracja i logowanie użytkowników (JWT).
2. Lista gier – z filtrowaniem po tytule i gatunku.
3. Możliwość dodawania, edytowania i usuwania gier przez administratora.
4. Asynchroniczne zadania (np. powiadomienie o nowej grze).
5. Panel admina Django.

Schemat architektury:
# Game Listing App

Aplikacja do przeglądania i zarządzania listą gier. Stworzona w ramach kursu ZTPAI.

Frontend(Next.js, Ant Design) -- Backend(Django REST Framework) -- PostgresSQL -- Celery/RabbitMQ

Opis projektu:
Jest to strona internetowa na której dostępne są różnorodne gru komputerowe. Można ich szukać zarówno po gatunku jak i nazwie.
Strona internetowa ma bardzo surowy stan, ALE przyjemny dla oka, przez co każdy użytkownik może cieszyć się gdy z niej korzysta.



