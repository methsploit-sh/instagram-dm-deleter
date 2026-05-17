import asyncio
from playwright.async_api import async_playwright

# Supported languages — maps UI language to selectors used in the script
LANGUAGES = {
    "tr": {
        "info_btn":    "Konuşma Bilgileri",
        "delete_chat": "Sohbeti sil",
        "confirm":     "Sil",
    },
    "en": {
        "info_btn":    "Conversation Information",
        "delete_chat": "Delete Chat",
        "confirm":     "Delete",
    },
    "de": {
        "info_btn":    "Informationen zur Unterhaltung",
        "delete_chat": "Chat löschen",
        "confirm":     "Löschen",
    },
    "fr": {
        "info_btn":    "Informations sur la conversation",
        "delete_chat": "Supprimer la discussion",
        "confirm":     "Supprimer",
    },
    "es": {
        "info_btn":    "Información de la conversación",
        "delete_chat": "Eliminar chat",
        "confirm":     "Eliminar",
    },
    "it": {
        "info_btn":    "Informazioni sulla conversazione",
        "delete_chat": "Elimina chat",
        "confirm":     "Elimina",
    },
    "pt": {
        "info_btn":    "Informações da conversa",
        "delete_chat": "Excluir conversa",
        "confirm":     "Excluir",
    },
    "ar": {
        "info_btn":    "معلومات المحادثة",
        "delete_chat": "حذف المحادثة",
        "confirm":     "حذف",
    },
    "ru": {
        "info_btn":    "Сведения о переписке",
        "delete_chat": "Удалить чат",
        "confirm":     "Удалить",
    },
    "ja": {
        "info_btn":    "会話情報",
        "delete_chat": "チャットを削除",
        "confirm":     "削除",
    },
    "ko": {
        "info_btn":    "대화 정보",
        "delete_chat": "채팅 삭제",
        "confirm":     "삭제",
    },
    "zh": {
        "info_btn":    "对话信息",
        "delete_chat": "删除聊天",
        "confirm":     "删除",
    },
}


async def detect_language(page):
    """
    Detect the Instagram UI language by checking which info button
    aria-label is present in the DOM. Falls back to English if unknown.
    """
    for code, strings in LANGUAGES.items():
        try:
            el = await page.query_selector(
                f'svg[aria-label="{strings["info_btn"]}"]'
            )
            if el:
                print(f"[INFO] Language detected: {code.upper()}")
                return strings
        except Exception:
            pass
    print("[WARN] Language not detected — falling back to English")
    return LANGUAGES["en"]


async def get_conversations(page):
    """Return all visible conversation button elements from the DM list."""
    result = []
    items = await page.query_selector_all('div[role="button"]')
    for item in items:
        img = await item.query_selector('img[alt="user-profile-picture"]')
        if img:
            result.append(item)
    return result


async def delete_all_instagram_chats():
    async with async_playwright() as p:

        # Launch a persistent browser context so the login session is saved
        # across runs — user only needs to log in once
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\Archy\AppData\Local\Playwright\instagram_session",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.bring_to_front()

        print("=" * 45)
        print("      Instagram DM Deleter")
        print("=" * 45)

        # Navigate to Instagram home page
        await page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # If not logged in, wait for the user to log in manually
        if "login" in page.url or "accounts" in page.url:
            print("[ACTION] Please log in to Instagram in the browser window.")
            print("[ACTION] Press Enter here when you are done...")
            input()

        # Go to the DM inbox
        print("[INFO] Navigating to Direct Messages...")
        await page.goto("https://www.instagram.com/direct/", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # Open the first available conversation to detect the UI language
        conversations = await get_conversations(page)
        if conversations:
            try:
                await conversations[0].click(timeout=3000)
                await page.wait_for_timeout(1000)
            except Exception:
                pass

        # Detect which language Instagram is using
        strings = await detect_language(page)

        # Return to the DM inbox before starting the deletion loop
        await page.goto("https://www.instagram.com/direct/", wait_until="domcontentloaded")
        await page.wait_for_timeout(1500)

        count = 0        # total deleted conversations
        fail_streak = 0  # consecutive failures — exits loop at 5

        print("[INFO] Starting deletion loop...\n")

        while fail_streak < 5:

            # Re-fetch the conversation list on every iteration
            # to avoid stale DOM references after deletions
            conversations = await get_conversations(page)

            if not conversations:
                fail_streak += 1
                print(f"[WARN] No conversations found ({fail_streak}/5)...")
                await page.wait_for_timeout(800)
                continue

            fail_streak = 0
            item = conversations[0]

            # Get the display name of the conversation
            try:
                name_el = await item.query_selector('span[title]')
                name = await name_el.get_attribute('title') if name_el else f"Chat {count + 1}"
            except Exception:
                name = f"Chat {count + 1}"

            print(f"[->] Processing: '{name}'")

            # Step 1 — Click the conversation to open it
            try:
                await item.click(timeout=3000)
            except Exception:
                print("[WARN] Click failed, retrying...")
                await page.wait_for_timeout(500)
                continue

            # Step 2 — Click the info (i) button to open the details panel
            try:
                info_btn = await page.wait_for_selector(
                    f'svg[aria-label="{strings["info_btn"]}"]',
                    timeout=2000
                )
                await info_btn.click()
            except Exception:
                print(f"[WARN] Info button not found for '{name}'")
                fail_streak += 1
                continue

            # Step 3 — Click "Delete Chat" inside the details panel
            try:
                delete_btn = await page.wait_for_selector(
                    f'text={strings["delete_chat"]}',
                    timeout=2000
                )
                await delete_btn.click()
            except Exception:
                print(f"[WARN] Delete chat option not found for '{name}'")
                await page.keyboard.press('Escape')
                fail_streak += 1
                continue

            # Step 4 — Confirm the deletion in the dialog
            try:
                confirm_btn = await page.wait_for_selector(
                    f'button:has-text("{strings["confirm"]}")',
                    timeout=2000
                )
                await confirm_btn.click()
                count += 1
                print(f"[OK] Deleted [{count}]: '{name}'")
                # Brief pause to let the DOM update before the next iteration
                await page.wait_for_timeout(300)
            except Exception:
                print(f"[WARN] Confirm button not found for '{name}'")
                await page.keyboard.press('Escape')
                fail_streak += 1

        print(f"\n[DONE] Deleted {count} conversation(s) in total.")
        input("Press Enter to close the browser...")
        await browser.close()


asyncio.run(delete_all_instagram_chats())