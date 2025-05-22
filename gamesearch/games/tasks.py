from celery import shared_task
import time

@shared_task
def sample_task(message):
    print(f"Start zadania: {message}")
    time.sleep(5)
    return f"Gotowe: {message}"

@shared_task
def notify_game_created(title):
    print(f"Dodano nową grę: {title}")
    return f"Zadanie zakończone dla: {title}"

@shared_task
def test_log():
    print("To jest test Celery")
