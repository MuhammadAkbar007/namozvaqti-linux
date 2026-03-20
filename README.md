# 🕌 NamozVaqti (Waybar Prayer Times)

A lightweight Linux prayer time system with:

* 📊 Waybar integration (live next prayer + tooltip)
* 🔔 Desktop notifications (with sound)
* ⚡ Ultra-efficient scheduler (event-driven, not polling-heavy)
* 💾 Monthly caching (offline-first behavior)

---

## 📦 Features

* Shows **next prayer** in Waybar:

  ```
  Asr 16:38 (in 1h 12m)
  ```

* Tooltip shows full day:

  ```
  Fajr     04:58
  Sunrise  06:17
  Dhuhr    12:25
  Asr      16:38
  Maghrib  18:28
  Isha     19:41
  ```

* Sends notification + sound exactly at prayer time

* Updates Waybar instantly via **signal (no polling lag)**

---

## 📁 Project Structure

```
namozvaqti/
├── cache.py
├── fetch.py
├── parse.py
├── transform.py
├── service.py
├── format.py
├── notify.py
├── scheduler.py
├── time_utils.py
├── assets/
│   ├── prayer-notification.wav
│   └── mosque_transparent.png
└── scripts/
    └── test_waybar.py
```

---

## ⚙️Requirements

Install system dependencies:

```bash
sudo nala install python3 python3-pip waybar libnotify-bin pipewire
```

Install Python dependencies:

```bash
pip install requests beautifulsoup4 lxml
```

---

## 🚀 Setup (Fresh System)

### 1. Clone project

```bash
git clone https://github.com/MuhammadAkbar007/namozvaqti-linux.git
cd namozvaqti-linux
```

---

### 2. Setup virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or if using `uv`:

```bash
uv sync
```

---

### 3. Test Waybar script manually

```bash
python -m namozvaqti.scripts.test_waybar
```

Expected output:

```json
{"text": "Asr 16:38 (in 1h 12m)", "tooltip": "..."}
```

---

## 🧩 Waybar Integration

### 1. Create script wrapper

`~/.config/waybar/prayer.sh`

```bash
#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

cd ~/path/to/namozvaqti || exit

/home/akbar/akbarDev/pet-projects/namozvaqti/.venv/bin/python \
    -m namozvaqti.scripts.test_waybar
```

Make executable:

```bash
chmod +x ~/.config/waybar/prayer.sh
```

---

### 2. Add Waybar module

In `custom.jsonc`:

```json
"custom/prayer": {
    "exec": "~/.config/waybar/prayer.sh",
    "return-type": "json",
    "signal": 8,
    "tooltip": true
}
```

---

### 3. Add to Waybar layout

```json
"modules-right": [
    ...
    "custom/prayer",
    "clock"
]
```

---

### 4. Reload Waybar

```bash
pkill waybar && waybar
```

---

## 🔔 Scheduler (Notifications + Waybar Signal)

### 1. Test manually

```bash
python -m namozvaqti.scheduler
```

---

### 2. Create systemd user service

`~/.config/systemd/user/namozvaqti.service`

```ini
[Unit]
Description=Namoz Vaqti Scheduler
After=network.target

[Service]
ExecStart=/home/akbar/.local/bin/uv run -m namozvaqti.scheduler
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

---

### 3. Enable service

```bash
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable namozvaqti.service
systemctl --user start namozvaqti.service
```

---

### 4. Check status

```bash
systemctl --user status namozvaqti.service
```

Logs:

```bash
journalctl --user -u namozvaqti.service -f
```

---

## ⚡ How It Works

### Data Flow

```
fetch → parse → transform → cache → service → waybar/scheduler
```

---

### Runtime Behavior

1. On first run:

   * Fetches monthly data from API
   * Saves to:

     ```
     ~/.cache/namozvaqti/YYYY-MM.json
     ```

2. Every prayer:

   * Scheduler sleeps until next prayer timestamp
   * Sends notification
   * Sends Waybar signal (`SIGRTMIN+8`)

3. Waybar:

   * Updates instantly (no polling delay)

---

## 🌐 Offline Behavior

| Scenario               | Behavior                         |
| ---------------------- | -------------------------------- |
| Cached month exists    | ✅ Works normally                 |
| New month, no internet | ❌ Fails to fetch                 |
| After failure          | Waybar may show stale/empty data |

---

### 🔧 Recommended Improvement (Optional)

Preload next month:

Add to scheduler:

```python
from namozvaqti.service import ensure_month

now = datetime.now()
ensure_month(now.year, now.month)
ensure_month((now + timedelta(days=31)).year, (now + timedelta(days=31)).month)
```

---

## 🧪 Debugging

### Waybar shows nothing

Check:

```bash
~/.config/waybar/prayer.sh
```

Add debug:

```bash
~/.config/waybar/prayer.sh 2> /tmp/prayer.log
```

---

### "uv: command not found"

Fix PATH in script:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

### Notifications not working

Test:

```bash
notify-send "Test" "Hello"
```

Check sound:

```bash
pw-play file.wav
```

---

## 🔄 Reinstall Checklist

After OS reinstall:

1. Install dependencies
2. Clone repo
3. Setup venv / uv
4. Restore:

   * `~/.config/waybar/`
   * `~/.config/systemd/user/`
5. Enable service:

   ```bash
   systemctl --user enable namozvaqti.service
   systemctl --user start namozvaqti.service
   ```
6. Restart Waybar

---

## ✍️ Author
Created by [Akbar](https://github.com/MuhammadAkbar007).
