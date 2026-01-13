import json
from .api_client import APIClient

class AIClient:
    def __init__(self):
        # In a real scenario, this would hold API keys for OpenRouter/LocalLLM
        pass

    def process_user_request(self, user_input, selected_agent, language="pl"):
        """
        Simulates the AI processing pipeline.
        1. Parse intent.
        2. Call HexStrike API.
        3. Format response in target language.
        """

        # Mock Intent Analysis
        # If input looks like a target, we assume recon/scan
        response_text = ""

        if "help" in user_input.lower():
            return "Jestem HexStrike Nexus. Mogę pomóc Ci w rekonesansie, skanowaniu podatności i zadaniach CTF. Wybierz agenta i wydaj polecenie."

        # Simple heuristic to extract domain/target for the mock
        words = user_input.split()
        target = None
        for w in words:
            if "." in w and not w.endswith("."):
                target = w
                break

        if target:
            # 1. Select Tools (via HexStrike)
            tools_resp = APIClient.select_tools(target)
            tools = tools_resp.get("tools", []) if tools_resp else []

            # 2. Analyze/Plan (via HexStrike)
            analysis = APIClient.analyze_target(target)
            plan = analysis.get("plan", []) if analysis else []

            # 3. Generate Response (Mock Translation)
            response_text += f"<b>Cel:</b> {target}<br>"
            response_text += f"<b>Agent:</b> {selected_agent}<br>"
            response_text += "<br><b>Uruchamiam narzędzia:</b><br>"
            for tool in tools:
                response_text += f"- <code>{tool}</code><br>"

            response_text += "<br><b>Plan działania:</b><br>"
            for step in plan:
                response_text += f"- {step}<br>"

            response_text += "<br><i>Rozpoczynam wykonywanie zadań...</i>"

        else:
            response_text = "Nie zrozumiałem celu. Podaj domenę lub IP do przeskanowania."

        return response_text
