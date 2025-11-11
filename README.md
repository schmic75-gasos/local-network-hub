# 🏠 Local Network Hub

Kompletní lokální síťový hub s real-time chatem a sdílením souborů pro domácí síť.

## ✨ Funkce

### 💬 Real-time Chat
- WebSocket komunikace v reálném čase
- Podpora Markdown formátování
- Možnost posílat GIF/emoji
- Ukládání historie chatu na serveru
- Indikátor psaní
- Persistence dat i po restartu

### 📁 File Sharing (LAN Cloud)
- Nahrávání souborů (drag & drop)
- Stahování souborů
- Mazání souborů
- Real-time aktualizace pro všechny uživatele
- Podpora velkých souborů (až 500MB)
- Automatické ikony podle typu souboru

### 🎨 Moderní Design
- Responzivní design
- Pastelový gradient pozadí
- Plynulé animace
- WhatsApp-inspired chat UI

## 🚀 Instalace a Spuštění

### Požadavky
- Python 3.7+
- pip3
- macOS (nebo Linux/Windows s úpravami)

### Rychlý Start

1. **Nastavte oprávnění pro spouštěcí skript:**
\`\`\`bash
chmod +x start.sh
\`\`\`

2. **Spusťte server:**
\`\`\`bash
./start.sh
\`\`\`

Server se automaticky spustí na portu 5000.

### Manuální Instalace

1. **Nainstalujte závislosti:**
\`\`\`bash
pip3 install -r requirements.txt
\`\`\`

2. **Spusťte server:**
\`\`\`bash
python3 server.py
\`\`\`

## 🌐 Přístup

### Z tohoto zařízení:
\`\`\`
http://localhost:5000
\`\`\`

### Z jiných zařízení v síti:
\`\`\`
http://[VAŠE_LOKÁLNÍ_IP]:5000
\`\`\`

Vaši lokální IP adresu najdete:
- macOS: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- Windows: `ipconfig`
- Linux: `ip addr show`

## 📂 Struktura Projektu

\`\`\`
local-network-hub/
├── server.py           # Python Flask server
├── index.html          # Frontend aplikace
├── requirements.txt    # Python závislosti
├── start.sh           # Spouštěcí skript
├── README.md          # Dokumentace
├── files/             # Složka pro sdílené soubory (vytvoří se automaticky)
└── data/              # Složka pro data (chat historie)
    └── chat_history.json
\`\`\`

## 🔧 Konfigurace

### Změna portu
V souboru `server.py` změňte:
\`\`\`python
socketio.run(app, host='0.0.0.0', port=5000, ...)
\`\`\`

### Maximální velikost souboru
V souboru `server.py` změňte:
\`\`\`python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
\`\`\`

### Počet uložených zpráv
V souboru `server.py` v funkci `handle_message`:
\`\`\`python
if len(history) > 500:  # Změňte 500 na požadovaný počet
\`\`\`

## 🛠️ API Endpoints

### Chat
- `WebSocket /` - Real-time chat komunikace
- `GET /api/chat/history` - Získat historii chatu
- `POST /api/chat/clear` - Vymazat historii chatu

### Files
- `GET /api/files` - Seznam všech souborů
- `POST /api/files/upload` - Nahrát soubor
- `GET /api/files/download/<filename>` - Stáhnout soubor
- `DELETE /api/files/delete/<filename>` - Smazat soubor

### Health
- `GET /health` - Health check

## 🎯 Použití

### Chat
1. Otevřete chat kliknutím na kartu "Chat"
2. Napište zprávu a stiskněte Enter nebo klikněte na "Odeslat"
3. Pro Markdown: klikněte na "📝 Markdown" a používejte Markdown syntaxi
4. Pro GIF: klikněte na "🎬 GIF" a vyberte emoji

### Sdílení Souborů
1. Otevřete "Sdílené Soubory"
2. Přetáhněte soubory do upload oblasti nebo klikněte pro výběr
3. Soubory se automaticky nahrají na server
4. Všichni uživatelé v síti uvidí nové soubory okamžitě

## 🔒 Bezpečnost

⚠️ **DŮLEŽITÉ**: Tento hub je určen pouze pro použití v **důvěryhodné lokální síti**.

- Nepoužívejte na veřejném internetu bez dodatečného zabezpečení
- Nepřidávejte citlivé soubory
- Doporučujeme použít firewall

## 🐛 Řešení Problémů

### Server se nespustí
- Zkontrolujte, zda je Python 3 nainstalován: `python3 --version`
- Zkontrolujte, zda jsou nainstalovány závislosti: `pip3 list`

### Nelze se připojit z jiného zařízení
- Zkontrolujte, zda jsou obě zařízení ve stejné síti
- Zkontrolujte firewall nastavení
- Ujistěte se, že používáte správnou IP adresu

### Chat nefunguje
- Zkontrolujte konzoli prohlížeče (F12) pro chyby
- Ujistěte se, že server běží
- Zkuste obnovit stránku

## 📝 Licence

Tento projekt je open-source a volně použitelný pro osobní účely.

## 🤝 Podpora

Pro problémy nebo dotazy vytvořte issue nebo kontaktujte vývojáře.

---

Vytvořeno s ❤️ pro lokální síťové komunity
