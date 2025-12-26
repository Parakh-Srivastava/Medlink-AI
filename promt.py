import google.generativeai as genai
import json

class AI:
    @staticmethod
    def generate(api_key, user_input):
        # Configure the SDK
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel("gemini-3-flash-preview") # Use flash for speed/JSON

        # Create the prompt for your 3-part JSON structure
        prompt = f"""
        Act as a First Aid Assistant. Respond ONLY with a valid JSON object.
        
        Structure:
        {{
          "responseHeading": "The specific injury name (String)",
          "responseBody": ["Step 1", "Step 2", "Step 3", "Step 4"],
          "responseConclusion": "Advice on finding a doctor (String) ending with 'Baingan'"
        }}
        
        User Query: {user_input}
        """

        try:
            response = model.generate_content(prompt)
            # Return the text so Flask can catch it
            return response.text
        except Exception as e:
            return json.dumps({
                "responseHeading": "API Error",
                "responseBody": str(e),
                "responseConclusion": "Error."
            })