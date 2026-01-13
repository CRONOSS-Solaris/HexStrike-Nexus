# HexStrike Nexus (v1.0) - Compatible with HexStrike AI v6.0

Graficzny i inteligentny interfejs (Mission Control) dla **HexStrike AI MCP Server v6.0**.
Nexus nie wymyśla koła na nowo - jest nakładką sterującą potężnym silnikiem HexStrike.

## 🏗️ Architektura (HexStrike v6.0)

System opiera się na architekturze wieloagentowej MCP (Model Context Protocol):
1.  **AI Brain (Nexus)**: Tłumaczy intencje użytkownika na komendy MCP.
2.  **HexStrike MCP Server**: Backend wykonawczy (Python).
3.  **Intelligent Decision Engine**: Wybiera odpowiednie narzędzia i parametry.
4.  **12+ Autonomous AI Agents**: Specjaliści od zadań (Bug Bounty, CTF, Exploit Dev).
5.  **150+ Security Tools**: Warstwa wykonawcza (Nmap, Nuclei, Amass, Ghidra).

## 🚀 Kluczowe Funkcje

### 1. Zero-Config Installation ("HexStrike First")
Skrypt `install.py` automatycznie przygotowuje środowisko, klonuje repozytorium HexStrike Core i instaluje brakujące narzędzia (apt/go/docker).

### 2. Live Mission Control
- **Live Console**: Podgląd surowych logów z silnika w czasie rzeczywistym (`/api/logs`).
- **Telemetry**: Monitorowanie CPU, RAM oraz aktywnych procesów (`/api/telemetry`).
- **Process Management**: Możliwość zatrzymywania procesów bezpośrednio z GUI (`/api/processes/terminate`).

### 3. Smart Caching Visualization
Podgląd efektywności systemu cache (`/api/cache/stats`) - Hits, Misses, Cache Size.

### 4. Agent Selector (v6.0 Compatible)
Wsparcie dla wszystkich głównych agentów HexStrike:
- 🕵️ **BugBountyWorkflowManager**: Automatyzacja testów webowych.
- 🏴 **CTFWorkflowManager**: Rozwiązywanie zadań CTF i inżynieria wsteczna.
- 🐛 **CVEIntelligenceManager**: Analiza zagrożeń i CVE.
- 💣 **AIExploitGenerator**: Tworzenie exploitów.

### 5. Raportowanie i Baza Danych
- Historia czatów zapisywana w SQLite.
- Wyniki skanowania cache'owane w `results_cache`.
- Generowanie raportów PDF (wielojęzyczne: PL/EN).

## 📡 API Reference Implementation

Nexus implementuje obsługę kluczowych endpointów HexStrike v6.0:
- `GET /health` - Status serwera.
- `POST /api/intelligence/analyze-target` - Główny silnik decyzyjny.
- `POST /api/intelligence/select-tools` - Dobór narzędzi.
- `GET /api/telemetry` - Metryki systemowe.
- `GET /api/logs` - Logi operacyjne.
- `GET /api/cache/stats` - Statystyki cache.
- `POST /api/processes/terminate/<pid>` - Zarządzanie procesami.

## 🛠️ Instalacja i Uruchomienie

1. **Uruchom Bootstrapper**:
   ```bash
   python3 hexstrike_nexus/install.py
   ```
2. **Uruchom Nexus Dashboard**:
   ```bash
   python3 hexstrike_nexus/main.py
   ```

## Wymagania
- Python 3.8+
- PyQt6 (GUI)
- Docker (dla izolacji narzędzi)
- Git (dla pobierania repozytoriów)
