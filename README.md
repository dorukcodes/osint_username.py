# 🕵️ Doruk OSINT Tool

Minimal ve hızlı çalışan, çoklu platformlarda kullanıcı adı (username) arayan **GUI tabanlı OSINT aracı**.

---

## ⚡ Features

* 🔍 20+ platformda username tarama
* ⚡ Multi-thread scanning (hızlı sonuç)
* 🧠 False-positive azaltma (akıllı kontrol)
* 📊 Canlı progress (%)
* 📁 Otomatik JSON export
* 🖥️ Terminal tarzı hacker arayüzü

---

## 🖼️ Preview

![preview](screenshot.png)

---

## ⚙️ Installation

```bash
git clone https://github.com/dorukcodes/doruk-osint-tool.git
cd doruk-osint-tool
pip install requests
```

---

## ▶️ Usage

```bash
python doruk_osint.py
```

### Steps:

* Username gir
* SCAN tuşuna bas
* Sonuçları canlı takip et

---

## 📂 Output

Sonuçlar otomatik olarak kaydedilir:

```bash
username_results.json
```

### Example:

```json
{
  "found": [["GitHub", "https://github.com/example"]],
  "miss": ["Instagram"],
  "blocked": ["Kaggle"]
}
```

---

## 🧠 Tech Stack

* Python
* Tkinter (GUI)
* Requests
* Threading

---

## ⚠️ Disclaimer

Bu araç yalnızca **eğitim ve araştırma amaçlıdır**.
Her türlü kullanım sorumluluğu kullanıcıya aittir.

---

## 👨‍💻 Developer

**dorukcodes**
GitHub: https://github.com/dorukcodes
