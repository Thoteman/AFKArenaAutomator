# AutoAFK - AFK Arena Automation Bot

AutoAFK is a GUI-based bot for automating daily tasks in **AFK Arena**, built with Python and `ttkbootstrap`. It interfaces with Android emulators to automate in-game actions like claiming rewards, completing battles, and more — so you can focus on the fun, not the grind.

> ⚠️ Currently in **Beta**: many features are functional, but some tasks are still under development. Feedback welcome!

---

## Features

* ✅ Beautiful, customizable GUI
* ✅ Auto-connect to Android emulator via `adb`
* ✅ Task toggling with persistent settings
* ✅ Live log output with timestamps
* ✅ Modular task categories:

  * Campaign
    * ✅ Claim afk rewards
    * ✅ Claim fast rewards (You choose how many times)
    * ✅ Attempt Campaign Battle
  * Dark Forest
    * ✅ Claim and send bounty board
    * ❌ Send bounty board based on task
    * ❌ Claim 10 free staves from weekly Ghoulish Gallery
    * ✅ Claim Trease Scramble rewards
    * ✅ Attack in Arena of Heroes (You choose how many times)
    * ✅ Claim Gladiator Coins
    * ❌ Bet on Legend's Tournament
    * ✅ Claim Temporal Fountain
    * ✅ Attempt King's Tower Battle
    * ❌ Arcane Labyrinth
  * Ranhorn
    * ❌ Claim wall of Legends Milestones
    * ❌ Buy from Store
    * ❌ Level Resonating Crystal
    * ❌ Guild Hunt
    * ❌ Twisted Realm
    * ❌ Claim Oak Inn gifts
    * ❌ Pull for Furniture
  * Misc
    * ✅ Claim Friendship Points
    * ✅ Send out Mercenaries
    * ✅ Read (and delete) Mail
    * ❌ Use Bag Items
    * ❌ Claim Quests
* ⚙️ Auto-saves configuration to `config.ini`
* 🧠 Future plans:
  * Turn all ❌ into ✅
  * Multi-emulator support
  * Task scheduling

---

## 📸 Screenshots

> Add screenshots here of the GUI, task toggles, logs, etc.

---

## 🧩 Requirements

* Python 3.9+
* Android emulator (e.g. LDPlayer, BlueStacks with ADB enabled)
* Dependencies (installed via `pip`):

```bash
pip install -r requirements.txt
```

---

## 🛠️ Setup & Usage

1. **Clone the repo:**

```bash
git clone https://github.com/ThomasKnoops/autoafk.git
cd autoafk
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Start the bot:**

```bash
python main.py
```

4. **In the GUI:**

   * Use the sidebar to connect to emulator, run tasks, or take screenshots
   * Click `Settings` in the top menu to configure which tasks to automate
   * Don't forget to hit **Save** in the settings window before closing

---

## ⚙️ Configuration

Settings are saved in a local `config.ini` file. But everything can be done through GUI: File --> Settings

* Tasks are categorized and toggleable
* Global settings include:

  * `Max Attempts`
  * `Delay` between actions
  * Test Server option (optional)

---

## 💻 Emulator Setup

Make sure your emulator:

* Is running and ADB is enabled
* Appears in `adb devices` list
* Is pre-configured for AFK Arena
  * Language: English
  * Resolution: 1920x1080

> For multiple emulator instances, future support is planned — currently, one instance is supported at a time.

---

## ❗ Known Issues

* Only one emulator instance is currently supported
* Some tasks are placeholders or partially implemented

---

## 📬 Feedback & Contact

Have ideas or issues? Open an [issue](https://github.com/ThomasKnoops/autoafk/issues) or send a message.
Discord: https://discord.gg/zuvcJ7yRgN

---

## 📄 License

MIT License — free for personal or educational use.
