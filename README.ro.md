# ha-bnr-rate  
Componenta personalizata Home Assistant pentru preluarea si afisarea cursurilor oficiale de schimb valutar de la Banca Nationala a Romaniei (BNR)

## Functionalitati
- Senzor pentru fiecare moneda suportata (ex: EUR, USD, GBP)
- Actualizare automata la ora publicarii BNR (implicit 13:05)
- Afiseaza numele complet al monedei, multiplicatorul si ora ultimei actualizari
- Ocoleste actualizarile in weekend (sambata si duminica)

## Instalare

### Instalare manuala
1. Copiaza folderul `bnr_rate` in directorul `custom_components` din Home Assistant.
2. Reporneste Home Assistant.
3. Acceseaza **Setari → Dispozitive si servicii → Adauga integrare** si cauta **BNR Rate** pentru a adauga si configura integrarea din interfata grafica.

### Instalare prin HACS

[![Adauga integrarea in Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=petrisorcraciun&repository=ha-bnr-rate&category=integration)

1. In Home Assistant, acceseaza **HACS → Integrations → Custom repositories**.
2. Adauga acest repository (`https://github.com/petrisorcraciun/ha-bnr-rate`) ca integrare personalizata.
3. Cauta **BNR Rate** in HACS si instaleaza integrarea.
4. Reporneste Home Assistant.
5. Mergi la **Setari → Dispozitive si servicii → Adauga integrare** si cauta **BNR Rate** pentru configurare.

> **Nota:** Poti adauga sau elimina monedele suportate editand lista `AVAILABLE_CURRENCIES` din fisierul `const.py`.

## Atribute expuse
- `publishing_date`: Data cursului publicat
- `currency_name`: Numele complet al monedei
- `multiplier`: Multiplicatorul (ex: 1, 10, 100)
- `last_success_update`: Data/ora ultimei actualizari reusite

## Dependente

Aceasta integrare **nu** utilizeaza si nu necesita biblioteci Python suplimentare. Toate dependentele necesare sunt deja incluse in Home Assistant.

## Sursa de date

Cursurile valutare sunt preluate direct din feed-ul XML oficial al Bancii Nationale a Romaniei (BNR).

## Despre `const.py`

Fisierul `const.py` contine toate constantele principale utilizate de integrare. Poti personaliza comportamentul acesteia modificand urmatoarele valori:

- `DOMAIN`: Domeniul pentru integrare (nu ar trebui modificat)
- `BNR_API_URL`: URL-ul feed-ului XML BNR
- `BNR_XML_NAMESPACE`: Namespace-ul XML utilizat la parsare
- `CONF_CURRENCY`, `DEFAULT_NAME`, `DEFAULT_CURRENCY`, `DEFAULT_MULTIPLIER`: Valori implicite pentru configurare
- `MIN_TIME_BETWEEN_UPDATES`: Intervalul minim intre actualizari (tip `timedelta`)
- `AVAILABLE_CURRENCIES`: Lista monedelor suportate. Poti adauga sau elimina monede (codurile trebuie sa corespunda cu cele din XML-ul BNR)
- `BNR_UPDATE_HOUR`, `BNR_UPDATE_MINUTE`: Ora si minutul la care BNR publica de obicei noile cursuri (utilizat pentru programarea actualizarilor)
- `BNR_MAX_RETRIES`: Numarul de incercari in caz de esec
- `BNR_RETRY_INTERVAL`: Intervalul (in secunde) dintre incercari (ex: 300 pentru 5 minute)
- `BNR_SKIP_WEEKDAYS`: Zilele saptamanii (Python: Luni=0, Duminica=6) in care actualizarile sunt ocolite (implicit: [5, 6] pentru sambata si duminica)

> **Sugestie:** Daca adaugi un nou cod de moneda in `AVAILABLE_CURRENCIES`, adauga si numele complet in fisierul `currency_names.py` pentru o afisare imbunatatita in Home Assistant.

## Suport
- [GitHub](https://github.com/petrisorcraciun/ha-bnr-rate)

---
**Autor:** [petrisorcraciun](https://github.com/petrisorcraciun)
