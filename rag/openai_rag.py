import json

from openai import OpenAI


MODEL_NAME = "gpt-5.6-luna"


# =========================================================
# CLIENT
# =========================================================

def create_openai_client(api_key: str):
    return OpenAI(
        api_key=api_key
    )


# =========================================================
# VECTOR STORE
# =========================================================

def create_openai_vector_store(client):
    return client.vector_stores.create(
        name="Climate Policy Intelligence"
    )


# =========================================================
# UPLOAD PDF
# =========================================================

def upload_pdf_to_openai_store(
    client,
    vector_store,
    pdf_path,
):
    with open(pdf_path, "rb") as file:

        uploaded_file = client.files.create(
            file=file,
            purpose="assistants",
        )

    client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store.id,
        file_id=uploaded_file.id,
    )

    return uploaded_file


# =========================================================
# MASTER ANALYSIS
# =========================================================

def analyze_openai_reports(
    client,
    vector_store,
):
    prompt = """
Analyze the uploaded climate policy, ESG or sustainability reports.

Use ONLY evidence retrieved from the uploaded reports.

Return VALID JSON using exactly these keys:

executive_summary
climate_risks
adaptation
mitigation
net_zero
scope_emissions
sustainability_targets
water_and_drought
energy_transition
sdg_alignment
suggested_questions

Each value except suggested_questions must be an array
containing a maximum of 5 concise findings.

suggested_questions must contain exactly 5 short questions.

RULES:

- Do not use outside knowledge.
- Prefer quantitative evidence.
- Preserve percentages, emissions values, dates and target years.
- Do not repeat findings.
- Distinguish targets from completed actions.
- Keep each finding concise.
- If evidence is missing, return:
  ["Not found in the uploaded reports."]
"""

    response = client.responses.create(
        model=MODEL_NAME,

        input=prompt,

        reasoning={
            "effort": "low"
        },

        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [
                    vector_store.id
                ],
                "max_num_results": 8,
            }
        ],
    )

    text = response.output_text.strip()

    # Remove markdown JSON fences if present.
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)


# =========================================================
# CUSTOM QUESTION
# =========================================================

def ask_openai_question(
    client,
    vector_store,
    question,
):
    prompt = f"""
Answer the following question using ONLY evidence retrieved
from the uploaded reports.

QUESTION:

{question}

RULES:

- Do not invent information.
- Do not use unsupported outside knowledge.
- Preserve relevant numbers, percentages and dates.
- Mention the source document when possible.
- Clearly state when the requested information cannot be found.
- Keep the answer concise and analytical.
"""

    response = client.responses.create(
        model=MODEL_NAME,

        input=prompt,

        reasoning={
            "effort": "low"
        },

        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [
                    vector_store.id
                ],
                "max_num_results": 8,
            }
        ],
    )

    return response.output_text