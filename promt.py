from google import genai
import json

class AI:
    @staticmethod
    def generate(api_key, user_input):
        # CORRECT NEW SYNTAX: Initialize the Client
        client = genai.Client(api_key=api_key)
        
        # Using the stable 2025 model
        model_id = "gemini-2.5-flash" 

        prompt = f"""
        Act as a First Aid Assistant. Respond ONLY with a valid JSON object.
        Structure:
        {{
          "keyword" : "a single word describing the injury",
          "responseHeading": "The specific injury name (String)",
          "responseBody": ["Step 1", "Step 2", "Step 3", "Step 4"],
          "responseConclusion": "Advice on finding a doctor (String) ending with 'Stay safe!'"
        }}
        User Query: {user_input}
        """

        try:
            # CORRECT NEW SYNTAX: client.models.generate_content
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return json.dumps({
                "keyword" : "error",
                "responseHeading": "API Error",
                "responseBody": [f"Technical details: {str(e)}"],
                "responseConclusion": "Please check your API key. Stay safe!"
            })