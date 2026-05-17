# 🗑️ Instagram DM Deleter

> Automatically delete all your Instagram Direct Message conversations with one command.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Chromium-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

---

## What it does

Instagram DM Deleter opens your Instagram inbox and automatically:

1. Opens each conversation
2. Clicks the info button
3. Selects "Delete Chat"
4. Confirms the deletion

No manual clicking required. Just run the script and let it work.

> **Note:** This only removes conversations from **your side**.  
> The other person can still see the chat.

---

## Requirements

- Python 3.8 or higher
- Windows / macOS / Linux

---

## Installation

### Windows (one click)

1. Download or clone this repository
2. Double-click `install.bat`

### Manual (all platforms)

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Usage

```bash
python instagram_delete.py
```

1. A browser window will open automatically
2. Log in to your Instagram account if prompted
3. The script detects your UI language and starts deleting
4. Your session is saved — no need to log in again next time

To stop the script at any time, close the terminal window.

---

## Supported Languages

The script automatically detects your Instagram UI language.

| Language   | Code |
|------------|------|
| English    | en   |
| Turkish    | tr   |
| German     | de   |
| French     | fr   |
| Spanish    | es   |
| Italian    | it   |
| Portuguese | pt   |
| Arabic     | ar   |
| Russian    | ru   |
| Japanese   | ja   |
| Korean     | ko   |
| Chinese    | zh   |

---

## How it works

```
instagram.com/direct
        │
        ▼
  Open conversation
        │
        ▼
  Click ⓘ info button
        │
        ▼
  Click "Delete Chat"
        │
        ▼
  Confirm deletion
        │
        ▼
  Repeat until inbox is empty
```

---

## Disclaimer

This tool is intended for personal use only.  
Use it responsibly and at your own risk.  
It does not collect, store or transmit any of your personal data.

---

## License

MIT — see [LICENSE](LICENSE) for details.
