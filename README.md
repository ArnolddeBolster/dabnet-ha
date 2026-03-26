# dabnet-ha
DAB NET radio track cover

# 🎵 DAB NET Receiver — Home Assistant Integration

Een volledig custom Home Assistant integratie voor DAB NET radio‑ontvangers.  
Deze integratie maakt het mogelijk om:

- 📻 Radiozenders te selecteren  
- 🔊 Volume te regelen  
- ▶️ Afspelen / pauzeren / stoppen  
- 🖼️ Cover‑art en metadata op te halen  
- 🎚️ Sound‑modes te tonen  
- 🧼 Een opgeschoonde titel (`clean_title`) te gebruiken  
- 🧩 Volledig te bedienen via een `media_player` entity  

Deze integratie is ontworpen om perfect samen te werken met geavanceerde UI‑kaarten zoals **button-card**.

---

## 🚀 Functies

| Functie | Ondersteund |
|--------|-------------|
| Power on/off | ✔ |
| Play / Pause / Stop | ✔ |
| Volume set | ✔ |
| Mute | ✔ (optioneel, afhankelijk van API) |
| Source select (zenders) | ✔ |
| Sound mode | ✔ |
| Cover art | ✔ |
| Clean title | ✔ |
| DataUpdateCoordinator | ✔ |
| Config Flow (UI setup) | ✔ |
| HACS ondersteuning | ✔ |

---

## 📦 Installatie via HACS

1. Open **HACS → Integrations**
2. Klik rechtsboven op **Custom repositories**
3. Voeg toe:

https://github.com/ArnolddeBolster/dabnet-ha (github.com in Bing)


4. Kies categorie **Integration**
5. Installeer **DAB NET Receiver**
6. Herstart Home Assistant
7. Ga naar **Instellingen → Integraties**
8. Voeg **DAB NET Receiver** toe en vul het IP‑adres van je DAB NET apparaat in

---

## 🛠️ Handmatige installatie

1. Download deze repository als ZIP  
2. Pak uit in:


3. Herstart Home Assistant

---

## ⚙️ Configuratie

De integratie gebruikt een **config flow**, dus configuratie gebeurt volledig via de UI.

### Vereist:

- `host`: IP‑adres van je DAB NET receiver

### Optioneel:

- `name`: Naam van de entity
- `poll_interval`: Update-interval in seconden (standaard: 10)

---

## 🧩 Entities

De integratie maakt één `media_player` entity aan:


### Attributen:

| Attribuut | Beschrijving |
|----------|--------------|
| `media_title` | Titel van het nummer |
| `media_artist` | Artiest |
| `sound_mode` | DAB / FM / etc. |
| `volume_level` | Volume (0.0–1.0) |
| `entity_picture` | Cover‑art URL |
| `clean_title` | Opgeschoonde titel |
| `source_list` | Beschikbare zenders |
| `source` | Huidige zender |

---

## 🎨 Voorbeeld button‑card

```yaml
type: custom:button-card
entity: media_player.dab_net_receiver
show_icon: false
show_state: false
show_name: false
# ... jouw volledige card-config hier ...

/api/status
/api/volume?set=0.5
/api/power?set=on
/api/channel?set=NPO%20Radio%202
/api/play
/api/pause
/api/stop

custom_components/dabnet/
├── __init__.py
├── manifest.json
├── config_flow.py
├── const.py
├── media_player.py
├── api.py
└── translations/
    ├── en.json
    └── nl.json
