import os
import promptlayer
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Load API Keys from environment variables
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize PromptLayer Client
promptlayer_client = promptlayer.PromptLayer(api_key=PROMPTLAYER_API_KEY, enable_tracing=True)
openai = promptlayer_client.openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic = promptlayer_client.anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
WITH_PROMPTLAYER = True

# Flask Application
app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the AI Trip Recommender API!"})


@app.route('/recommend_trip', methods=['POST'])
def recommend_trip():
    """ Generate a travel itinerary using a saved prompt in PromptLayer """

    try:
        # Extract user input
        data = request.get_json()
        destination = data.get("destination", "New York")
        duration = data.get("duration", "1 week")
        travel_preferences = data.get("preferences", "adventure, food, sightseeing")

        # Prepare template variables
        variables = {
            "destination": destination,
            "duration": duration,
            "preferences": travel_preferences
        }

        if WITH_PROMPTLAYER:
            response = promptlayer_client.run(
                prompt_name="ai-trip-recommender",
                input_variables=variables,
                # prompt_release_label=os.getenv("ENV"),
                tags=["web-app", "flask-api"]
            )

            pl_request_id = response["request_id"]
            trip_plan = response["prompt_blueprint"]["prompt_template"]["messages"][-1]['content'][0]['text']
        else:
            # Fetch stored prompt template from PromptLayer
            trip_template_prompt = promptlayer_client.templates.get(
                "ai-trip-recommender",
                {
                    "provider": "openai",
                    "input_variables": variables,
                    "label": os.getenv("ENV")
                }
            )

            # Call OpenAI through PromptLayer
            response, pl_request_id = openai.chat.completions.create(
                **trip_template_prompt['llm_kwargs'],
                return_pl_id=True
            )

            # Extract trip plan from response using openai native format
            trip_plan = response.choices[0].message.content

        # Associate request with the prompt template in PromptLayer
        promptlayer_client.track.prompt(
            request_id=pl_request_id,
            prompt_name="ai-trip-recommender",
            prompt_input_variables=variables
        )

        # Log metadata for analytics
        promptlayer_client.track.metadata(
            request_id=pl_request_id,
            metadata={
                "user_id": data.get("user_id", "guest"),
                "travel_preferences": travel_preferences
            }
        )

        # Score response quality (Optional: Based on certain criteria)
        promptlayer_client.track.score(
            request_id=pl_request_id,
            score=(100 if destination in trip_plan else 50),
        )

        return jsonify({
            "destination": destination,
            "trip_plan": trip_plan
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
