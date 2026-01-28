import os
from dotenv import load_dotenv
from .browser import Browser
from .agent import Agent
load_dotenv()


def main():
    user_data_dir = os.getenv("PW_USER_DATA_DIR", "profiles/default")
    headless = os.getenv("PW_HEADLESS", "0") == "1"

    browser = Browser(user_data_dir=user_data_dir, headless=headless)
    print("✅ Browser started (persistent session enabled).")
    print("Если нужно — залогинься вручную в открытом браузере.\n")

    agent = Agent(browser)

    try:
        task = input("Введите задачу агенту: ").strip()
        if not task:
            print("Пустая задача.")
            return
        result = agent.run(task, max_steps=25)
        print("\n--- RESULT ---")
        print(result)
    finally:
        browser.close()


if __name__ == "__main__":
    main()
