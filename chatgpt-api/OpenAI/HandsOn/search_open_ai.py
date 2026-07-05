import os
import json
import ssl
import time
import httpx
import truststore
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
assert api_key, "OPENAI_API_KEY is missing from .env"

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

client = OpenAI(
    api_key=api_key,
    http_client=httpx.Client(verify=ssl_context),
)

# models = client.models.list()

# for model in models.data:
#     print(model.id)

# test = client.moderations.create(
#     model="omni-moderation-latest",
#     input="ship a parcel"
# )

# print(test.results[0].flagged)

print("API key loaded successfully")

SEARCH_DATA = {
    "searchCapabilities": [
        {
            "id": "SHIP_PACKAGE",
            "presentation": {
                "title": "Ship a Package test",
                "subtitle": "Create and send a shipment test",
            },
            "intent": {
                "keywords": ["book", "create", "initiate"],
                "phrases": [
                    "book a shipment",
                    "create a shipment id",
                    "initiate a shipment request",
                    "Creating a tracking number",
                ],
            },
        },
        {
            "id": "SCHEDULE_PICKUP",
            "presentation": {
                "title": "Schedule a Pickup test",
                "subtitle": "Arrange a package pickup test",
            },
            "intent": {
                "keywords": ["initiate", "raise", "collect", "arrange"],
                "phrases": [
                    "arrange a pickup",
                    "schedule door-step pickup",
                    "create a collection request",
                    "arrange pickup for my shipment",
                ],
            },
        },
        {
            "id": "TRACK_SHIPMENT",
            "presentation": {
                "title": "Track a Package",
                "subtitle": "Check shipment status",
            },
            "intent": {
                "keywords": ["consignment"],
                "phrases": [
                    "track my consignment",
                    "my consignment",
                    "my shipment",
                    "my package",
                    "my parcel",
                ],
            },
        },
        {
            "id": "HOLD_MY_DELIVERY",
            "presentation": {
                "title": "Hold My Delivery",
                "subtitle": "Pause or reschedule delivery",
            },
            "intent": {
                "keywords": ["on hold"],
                "phrases": ["hold delivery", "delivery hold request"],
            },
        },
        {
            "id": "MANAGE_PREFERENCES",
            "presentation": {
                "title": "Manage Preferences",
                "subtitle": "Update delivery options",
            },
            "intent": {
                "keywords": ["customize", "alter", "modify", "update"],
                "phrases": [
                    "customize my preferences",
                    "my preferences",
                    "modify delivery options",
                ],
            },
        },
        {
            "id": "DELIVERY_UPDATES",
            "presentation": {
                "title": "Get Delivery Updates",
                "subtitle": "Manage notifications",
            },
            "intent": {
                "keywords": ["receive", "notify"],
                "phrases": [
                    "manage notifications",
                    "notify me",
                    "delivery notifications",
                ],
            },
        },
        {
            "id": "ADD_ADDRESS",
            "presentation": {
                "title": "Add My Address",
                "subtitle": "Save a delivery address",
            },
            "intent": {
                "keywords": ["residential", "office", "commercial"],
                "phrases": ["add address"],
            },
        },
        {
            "id": "ADD_ALTERNATIVE_DELIVERY_LOCATION",
            "presentation": {
                "title": "Add Alternate Delivery Location",
                "subtitle": "Change delivery destination",
            },
            "intent": {
                "keywords": ["another", "secondary", "alter"],
                "phrases": ["redirect to another location"],
            },
        },
        {
            "id": "DRIVER_INSTRUCTIONS",
            "presentation": {
                "title": "Add Driver Instructions",
                "subtitle": "Provide delivery instructions",
            },
            "intent": {
                "keywords": ["directions"],
                "phrases": ["driver instructions", "note to driver", "notify driver"],
            },
        },
        {
            "id": "PICKUP_HISTORY",
            "presentation": {
                "title": "Pickup History",
                "subtitle": "View previous pickups",
            },
            "intent": {
                "keywords": ["past", "list"],
                "phrases": [
                    "historical pickups",
                    "my pickups",
                    "show my pickup history",
                ],
            },
        },
        {
            "id": "SHIPPING_DISCOUNT",
            "presentation": {
                "title": "Get Discount",
                "subtitle": "Apply shipping offers",
            },
            "intent": {"keywords": ["coupons"], "phrases": ["discount coupons"]},
        },
        {
            "id": "MANAGE_PAYMENTS",
            "presentation": {
                "title": "Manage Payments",
                "subtitle": "Update payment details",
            },
            "intent": {
                "keywords": ["manage"],
                "phrases": ["modify payment methods", "modify payment options"],
            },
        },
        {
            "id": "MANAGE_PROFILE",
            "presentation": {
                "title": "Edit My Profile",
                "subtitle": "Update personal details",
            },
            "intent": {
                "keywords": ["manage", "modify"],
                "phrases": ["profile information"],
            },
        },
        {
            "id": "IN_STORE_RECEIPTS",
            "presentation": {
                "title": "My In-store Receipts",
                "subtitle": "View purchase history",
            },
            "intent": {
                "keywords": ["bill", "invoice"],
                "phrases": [
                    "in-store receipts",
                    "in-store transactions",
                    "store transactions",
                ],
            },
        },
        {
            "id": "UPS_STORE",
            "presentation": {
                "title": "Set My Favorite Store (The UPS Store)",
                "subtitle": "Choose preferred UPS location",
            },
            "intent": {
                "keywords": ["tupps", "outlet", "access point", "fetch"],
                "phrases": [
                    "my store",
                    "locate nearest ups store",
                    "nearest ups location",
                ],
            },
        },
        {
            "id": "PASSWORD_RESET",
            "presentation": {
                "title": "Reset Password",
                "subtitle": "Reset or recover your account password",
            },
            "intent": {
                "keywords": ["password", "passwd", "pswd", "reset", "forgot", "login"],
                "phrases": [
                    "reset password",
                    "forgot password",
                    "rst pswd",
                    "cannot log in",
                    "recover my account",
                    "change my password",
                ],
            },
        },
    ]
}

VALID_IDS = {item["id"] for item in SEARCH_DATA["searchCapabilities"]}


def moderate_query(user_query):
    raw = client.chat.completions.with_raw_response.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": 'You are a content moderator. Reply ONLY with valid JSON: {"is_safe": true/false, "reason": "..."}. Flag harmful, violent, or abusive content as unsafe. Normal shipping/logistics queries are always safe.',
            },
            {"role": "user", "content": user_query},
        ],
        response_format={"type": "json_object"},
    )
    response = raw.parse()
    print("RPM limit:     ", raw.headers.get("x-ratelimit-limit-requests"))
    print("RPM remaining: ", raw.headers.get("x-ratelimit-remaining-requests"))
    print("RPM reset in:  ", raw.headers.get("x-ratelimit-reset-requests"))
    print("TPM limit:     ", raw.headers.get("x-ratelimit-limit-tokens"))
    print("TPM remaining: ", raw.headers.get("x-ratelimit-remaining-tokens"))
    result = json.loads(response.choices[0].message.content)
    return {
        "is_safe": result.get("is_safe", True),
        "flagged_categories": [result["reason"]] if not result.get("is_safe") else [],
    }


# def moderate_query(user_query):
#     """Checks whether the search query is safe to process."""
#     moderation = client.moderations.create(
#         model="omni-moderation-latest", input=user_query
#     )

#     result = moderation.results[0]

#     flagged_categories = [
#         category
#         for category, is_flagged in result.categories.model_dump().items()
#         if is_flagged
#     ]

#     return {"is_safe": not result.flagged, "flagged_categories": flagged_categories}

# def moderate_query(user_query):
#     return {"is_safe": True, "flagged_categories": []}


def search_ups_capability(user_query):
    # Step 1: moderation
    safety = moderate_query(user_query)

    if not safety["is_safe"]:
        return {
            "capability_id": "NO_RESULT",
            "confidence": 1.0,
            "reason": "This search cannot be processed.",
            "moderated": True,
        }

    # Step 2: strict intent search
    prompt = f"""
You are a strict intent-search engine for a UPS mobile app.

Your task is to match a user's search ONLY to one capability ID that exists
in the provided capability catalog.

Rules:
1. Understand typos, abbreviations, spelling mistakes, synonyms, and natural language.
2. Return "NO_RESULT" for anything unrelated to the catalog.
3. Never invent a capability ID or feature.
4. Return "NO_RESULT" if confidence is below 0.70.
5. "shop a parcel" may mean "ship a parcel" and should map to SHIP_PACKAGE.
6. "rst pswd" should map to PASSWORD_RESET.
7. "biryani", "movies", and "weather" must return NO_RESULT.

Capability catalog:
{json.dumps(SEARCH_DATA, indent=2)}

User search:
{user_query}
"""

    print("Calling cloud model: gpt-5.4-mini...")

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "ups_search_result",
                "schema": {
                    "type": "object",
                    "properties": {
                        "capability_id": {
                            "type": "string",
                            "enum": sorted(VALID_IDS) + ["NO_RESULT"],
                        },
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "reason": {"type": "string"},
                    },
                    "required": ["capability_id", "confidence", "reason"],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        },
    )

    print("Cloud model response received.")

    result = json.loads(response.output_text)

    # Step 3: backend guardrail — do not trust model output blindly
    if result["capability_id"] not in VALID_IDS or result["confidence"] < 0.70:
        return {
            "capability_id": "NO_RESULT",
            "confidence": result["confidence"],
            "reason": "No matching UPS mobile app feature found.",
            "moderated": False,
        }

    result["moderated"] = False
    return result


while True:
    query = input("\nSearch UPS app (type 'exit' to stop): ").strip()

    if query.lower() == "exit":
        print("Search stopped.")
        break

    if not query:
        continue

    result = search_ups_capability(query)
    print(json.dumps(result, indent=2))
