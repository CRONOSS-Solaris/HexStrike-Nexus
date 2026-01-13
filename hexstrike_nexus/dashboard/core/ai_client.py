import json
from .api_client import APIClient
from .reporter import Reporter

class AIClient:
    def __init__(self):
        pass

    def process_user_request(self, user_input, selected_agent, language="pl"):
        # Mock Intent Analysis
        response_text = ""

        # Basic help
        if "help" in user_input.lower():
            if language == "pl":
                return "Jestem HexStrike Nexus. Mogę pomóc Ci w rekonesansie, skanowaniu podatności i zadaniach CTF. Wybierz agenta i wydaj polecenie."
            else:
                return "I am HexStrike Nexus. I can help with recon, vulnerability scanning, and CTF tasks. Select an agent and give a command."

        # Simple heuristic to extract domain/target
        words = user_input.split()
        target = None
        for w in words:
            if "." in w and not w.endswith(".") and len(w) > 3:
                target = w
                break

        if target:
            # 1. Select Tools
            tools_resp = APIClient.select_tools(target)
            tools = tools_resp.get("tools", []) if tools_resp else []

            # 2. Analyze/Plan
            analysis = APIClient.analyze_target(target)
            plan = analysis.get("plan", []) if analysis else []

            # 3. Generate Report (Simulated completion)
            report_path = Reporter.generate_report(target, plan, language)

            # 4. Generate Response
            if language == "pl":
                response_text += f"<b>Cel:</b> {target}<br>"
                response_text += f"<b>Agent:</b> {selected_agent}<br>"
                response_text += "<br><b>Uruchamiam narzędzia:</b><br>"
                for tool in tools:
                    response_text += f"- <code>{tool}</code><br>"

                response_text += "<br><b>Plan działania:</b><br>"
                for step in plan:
                    response_text += f"- {step}<br>"

                response_text += "<br><i>Zadanie wykonane. Znaleziono potencjalne wektory ataku.</i><br>"
                response_text += f"<b>Raport gotowy:</b> <a href='file://{report_path}'>{report_path}</a>"
            else:
                response_text += f"<b>Target:</b> {target}<br>"
                response_text += f"<b>Agent:</b> {selected_agent}<br>"
                response_text += "<br><b>Starting tools:</b><br>"
                for tool in tools:
                    response_text += f"- <code>{tool}</code><br>"

                response_text += "<br><b>Execution Plan:</b><br>"
                for step in plan:
                    response_text += f"- {step}<br>"

                response_text += "<br><i>Task completed. Potential attack vectors found.</i><br>"
                response_text += f"<b>Report ready:</b> <a href='file://{report_path}'>{report_path}</a>"

        else:
            if language == "pl":
                response_text = "Nie zrozumiałem celu. Podaj domenę lub IP do przeskanowania."
            else:
                response_text = "I didn't understand the target. Please provide a domain or IP."

        return response_text
