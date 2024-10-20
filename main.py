from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

def search_wikipedia(query):

    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    browser.get(url)
    time.sleep(3)
    print(f"Открыта страница по запросу: {query}")

def list_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{paragraph.text}")
        if i % 5 == 0:
            user_input = input("Нажмите Enter для продолжения или введите 'stop' для выхода: ")
            if user_input.lower() == 'stop':
                break


def show_links():
    links = browser.find_elements(By.CSS_SELECTOR, "a")
    internal_links = [link for link in links if "wiki" in link.get_attribute('href')]

    print("\nСвязанные статьи:")
    for i, link in enumerate(internal_links[:10]): 
        print(f"{i + 1}. {link.text} - {link.get_attribute('href')}")

    choice = input("Введите номер статьи, чтобы перейти (или 'назад' для возврата): ")
    if choice.lower() == 'назад':
        return

    try:
        selected_index = int(choice) - 1
        if selected_index >= 0 and selected_index < len(internal_links):
            new_url = internal_links[selected_index].get_attribute('href')
            browser.get(new_url)
            time.sleep(3)
            list_paragraphs()
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Введите корректный номер.")


while True:
    query = input("Введите запрос для поиска на Википедии (или 'exit' для выхода): ")
    if query.lower() == 'exit':
        break

    search_wikipedia(query)

    while True:
        print("\nЧто вы хотите сделать дальше?")
        print("1. Листать параграфы статьи.")
        print("2. Перейти на связанную статью.")
        print("3. Выйти.")

        choice = input("Введите номер действия: ")
        if choice == '1':
            list_paragraphs()
        elif choice == '2':
            show_links()
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

browser.quit()
