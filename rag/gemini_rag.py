import os
import time

from google import genai
from pydantic import BaseModel, Field


MODEL_NAME = "gemini-3.8-flash"


# =========================================================
# STRUCTURED REPORT ANALYSIS SCHEMA
# =========================================================

class ReportAnalysis(BaseModel):

    executive_summary: list[str] = Field(
        description="Maximum 5 concise key findings."
    )

    climate_risks: list[str] = Field(
        description="Maximum 5 major physical or transition climate risks."
    )

    adaptation: list[str] = Field(
        description="Maximum 5 adaptation or resilience actions."
    )

    mitigation: list[str] = Field(
        description="Maximum 5 mitigation or emissions-reduction actions."
    )

    net_zero: list[str] = Field(
        description="Maximum 4 facts about net-zero targets and target years."
    )

    scope_emissions: list[str] = Field(
        description="Maximum 5 facts about Scope 1, 2 and 3 emissions or targets."
    )

    sustainability_targets: list[str] = Field(
        description="Maximum 5 measurable sustainability targets or KPIs."
    )

    water_and_drought: list[str] = Field(
        description="Maximum 4 findings about water scarcity, drought or water management."
    )

    energy_transition: list[str] = Field(
        description="Maximum 4 findings about renewable energy, efficiency or electrification."
    )

    sdg_alignment: list[str] = Field(
        description="Maximum 5 evidence-supported SDG alignments."
    )

    suggested_questions: list[str] = Field(
        description="Exactly 5 short document-specific follow-up questions."
    )

# =========================================================
# CLIENT
# =========================================================

def create_client(api_key: str):

    return genai.Client(
        api_key=api_key
    )


# =========================================================
# FILE SEARCH STORE
# =========================================================

def create_file_search_store(client):

    store = client.file_search_stores.create(
        config={
            "display_name": "Climate Policy Intelligence",
            "embedding_model": "models/gemini-embedding-2",
        }
    )

    return store


# =========================================================
# UPLOAD OPTIMIZED PDF
# =========================================================

def upload_pdf_path_to_store(
    client,
    store,
    pdf_path,
    display_name,
):

    operation = (
        client.file_search_stores.upload_to_file_search_store(
            file=pdf_path,

            file_search_store_name=store.name,

            config={
                "display_name": display_name,

                # Climate reports usually contain long contextual sections.
                # Moderate overlap helps avoid losing context across chunks.
                "chunking_config": {
                    "white_space_config": {
                        "max_tokens_per_chunk": 500,
                        "max_overlap_tokens": 50,
                    }
                },
            },
        )
    )

    while not operation.done:

        time.sleep(5)

        operation = client.operations.get(
            operation
        )

    return operation


# =========================================================
# ONE COMPREHENSIVE ANALYSIS REQUEST
# =========================================================

def analyze_reports(client, store):

    prompt = """
You are a climate-policy and sustainability research analyst.

Analyze the uploaded documents using ONLY evidence retrieved
through File Search.

Produce a comprehensive structured assessment.

IMPORTANT RULES

- Do not invent facts.
- Do not use unsupported outside knowledge.
- If evidence for a category is absent, state that clearly.
- Preserve numerical values exactly when possible.
- Capture percentages, emissions values, baseline years,
  target years, dates and deadlines.
- Clearly distinguish:
  current performance,
  completed actions,
  future actions,
  commitments,
  targets,
  risks.
- When multiple documents exist, distinguish between them.
- Mention document names where supported by retrieved evidence.
- Do not infer an SDG unless the document content supports
  the relationship.
- Suggested questions must be specific to the uploaded reports,
  not generic sustainability questions.
"""

    interaction = client.interactions.create(

        model=MODEL_NAME,

        input=prompt,

        tools=[
            {
                "type": "file_search",
                "file_search_store_names": [
                    store.name
                ],
            }
        ],

        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ReportAnalysis.model_json_schema(),
        },
    )

    analysis = ReportAnalysis.model_validate_json(
        interaction.output_text
    )

    return analysis.model_dump()


# =========================================================
# CUSTOM RAG QUESTION
# =========================================================

def ask_custom_question(
    client,
    store,
    question,
):

    prompt = f"""
You are a climate-policy and sustainability research assistant.

Answer the following question using ONLY retrieved evidence
from the uploaded reports.

QUESTION:
{question}

RULES:

- Do not invent information.
- If the answer cannot be supported by the reports, say so.
- Preserve important numbers, percentages and dates.
- Clearly separate evidence from interpretation.
- Mention source document names when available.
- Keep the answer analytical but readable.
"""

    interaction = client.interactions.create(

        model=MODEL_NAME,

        input=prompt,

        tools=[
            {
                "type": "file_search",
                "file_search_store_names": [
                    store.name
                ],
            }
        ],
    )

    return interaction.output_text