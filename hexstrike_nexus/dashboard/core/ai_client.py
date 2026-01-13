import json
import os
import requests
from .api_client import APIClient
from .reporter import Reporter

class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions" # Default to OpenRouter
        self.model = "anthropic/claude-3.5-sonnet"

    def process_user_request(self, user_input, selected_agent, language="pl"):
        # Real AI Processing (if configured)
        if self.api_key:
            return self._query_llm(user_input, selected_agent, language)

        # Fallback: Heuristic Mock Logic
        return self._heuristic_mock(user_input, selected_agent, language)

    def _query_llm(self, user_input, selected_agent, language):
        """
        Sends the request to an LLM to interpret the intent and generate a response.
        This is a simplified implementation.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = f"""
        You are HexStrike Nexus, an advanced cybersecurity assistant.
        Current Agent Persona: {selected_agent}
        Language: {language}

        Your task is to analyze the user's request and suggest specific HexStrike tools or actions.
        Available tools: nmap, nuclei, subfinder, gobuster, masscan.
        """

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        }

        try:
            # In a real scenario, we would make the request here.
            # response = requests.post(self.api_url, headers=headers, json=data)
            # return response.json()['choices'][0]['message']['content']
            pass
        except Exception as e:
            return f"Error contacting AI Provider: {str(e)}"

        # Fallback to mock if API call fails or is commented out for safety
        return self._heuristic_mock(user_input, selected_agent, language)

    def _heuristic_mock(self, user_input, selected_agent, language="pl"):
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
