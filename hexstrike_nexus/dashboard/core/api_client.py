import requests
from .config import Config

class APIClient:
    @staticmethod
    def get_telemetry():
        try:
            response = requests.get(f"{Config.SERVER_URL}/api/telemetry", timeout=1)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    @staticmethod
    def get_logs():
        try:
            response = requests.get(f"{Config.SERVER_URL}/api/logs", timeout=1)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    @staticmethod
    def get_cache_stats():
        try:
            response = requests.get(f"{Config.SERVER_URL}/api/cache/stats", timeout=1)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    @staticmethod
    def terminate_process(pid):
        try:
            # Send empty json to ensure Content-Length > 0 and valid JSON for mock server parsing
            response = requests.post(f"{Config.SERVER_URL}/api/processes/terminate/{pid}", json={}, timeout=2)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    @staticmethod
    def analyze_target(target, analysis_type="recon"):
        try:
            payload = {"target": target, "analysis_type": analysis_type}
            response = requests.post(f"{Config.SERVER_URL}/api/intelligence/analyze-target", json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
        return {"error": "Failed to connect to HexStrike Server"}

    @staticmethod
    def select_tools(target):
        try:
            payload = {"target": target}
            response = requests.post(f"{Config.SERVER_URL}/api/intelligence/select-tools", json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None
