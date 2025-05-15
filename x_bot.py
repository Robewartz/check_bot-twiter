from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import os

# Укажите путь к существующему профилю Chrome в Linux
user_data_dir = "/home/server/.config/google-chrome"
profile_name = "Profile 1"

# Настройки ChromeOptions для использования существующего профиля
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_name}")
chrome_options.add_argument("--detach") # Оставляем браузер открытым после завершения скрипта

# Инициализация WebDriver с ChromeOptions
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def find_and_comment_on_tweets():
    try:
        tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')
        if tweets:
            with open("comments.txt", "r", encoding='utf-8') as f:
                comments = [line.strip() for line in f]
            if comments:
                num_comments = random.randint(2, 3)
                commented_count = 0
                random.shuffle(tweets) # Перемешиваем твиты для случайного выбора

                for tweet in tweets:
                    if commented_count < num_comments:
                        try:
                            if comment_on_tweet(tweet, random.choice(comments)):
                                commented_count += 1
                                wait_time = random.randint(900, 3600) # Задержка 15-60 минут (в секундах)
                                print(f"Следующий комментарий через {wait_time // 60} минут.")
                                time.sleep(wait_time)
                        except Exception as e:
                            print(f"Ошибка при попытке комментирования твита: {e}")
                    else:
                        break
            else:
                print("Файл comments.txt пуст.")
        else:
            print("На странице не найдено твитов.")
    except FileNotFoundError:
        print("Ошибка: Не найден файл comments.txt")
    except Exception as e:
        print(f"Произошла ошибка при поиске и комментировании твитов: {e}")

def comment_on_tweet(tweet, comment):
    try:
        reply_button = tweet.find_element(By.XPATH, './/div[@data-testid="reply"]')
        reply_button.click()
        time.sleep(2)

        comment_field = driver.find_element(By.XPATH, '//div[@aria-label="Напишите ответ"]')
        comment_field.send_keys(comment)
        time.sleep(1)

        tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
        tweet_button.click()
        print(f"Успешно опубликован комментарий: '{comment}'")
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Произошла ошибка при комментировании: {e}")
        return False

def main():
    input("Откройте Twitter в браузере, выполните поиск по хэштегу и нажмите Enter здесь, чтобы бот начал комментировать...")
    while True:
        find_and_comment_on_tweets()
        input("Выполнили новый поиск? Нажмите Enter, чтобы бот продолжил комментировать...")

if __name__ == "__main__":
    main()
