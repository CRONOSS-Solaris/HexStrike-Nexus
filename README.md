# HexStrike Nexus

Graficzny i inteligentny interfejs dla HexStrike MCP Server.

## Instalacja

1. Uruchom skrypt instalacyjny (Bootstrapper):
   ```bash
   python3 hexstrike_nexus/install.py
   ```
   Ten skrypt przygotuje środowisko, sklonuje repozytorium HexStrike Core i zainstaluje zależności.

## Uruchomienie

Aby uruchomić Dashboard:
```bash
python3 hexstrike_nexus/main.py
```

## Funkcje

- **Dashboard AI**: Inteligentny asystent tłumaczący polecenia na akcje HexStrike.
- **HexStrike Service Manager**: Automatyczne zarządzanie serwerem backendowym.
- **Live Telemetry**: Podgląd zasobów i procesów w czasie rzeczywistym.
- **Agent Selector**: Wybór specjalistycznych agentów (BugBounty, CTF, CVE).
- **Auto-Update**: Automatyczne aktualizacje komponentów Nexus i Core.

## Struktura

- `hexstrike_nexus/dashboard/`: Kod źródłowy GUI (PyQt6).
- `hexstrike_nexus/dashboard/core/`: Logika biznesowa i integracja z API.
- `hexstrike_nexus/mock_server.py`: Serwer symulacyjny (używany gdy brak pełnego HexStrike Core).
