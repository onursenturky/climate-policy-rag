import os
import tempfile

import streamlit as st

from rag.pdf_optimizer import (
    optimize_pdf,
    format_mb,
)

from rag.gemini_rag import (
    create_client as create_gemini_client,
    create_file_search_store,
    upload_pdf_path_to_store,
    analyze_reports as analyze_gemini_reports,
    ask_custom_question as ask_gemini_question,
)

from rag.openai_rag import (
    create_openai_client,
    create_openai_vector_store,
    upload_pdf_to_openai_store,
    analyze_openai_reports,
    ask_openai_question,
)


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Climate Policy Intelligence",
    page_icon="🌍",
    layout="wide",
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "client": None,
    "store": None,
    "provider": None,
    "indexed_signature": None,
    "analysis": None,
    "selected_section": "executive_summary",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HEADER
# =========================================================

st.title("🌍 Climate Policy Intelligence")

st.write(
    "AI-powered analysis for climate policy, "
    "ESG and sustainability reports."
)


# =========================================================
# 1 — PROVIDER
# =========================================================

st.divider()

st.subheader("1. Choose AI Provider")

provider = st.radio(
    "AI Provider",
    [
        "OpenAI",
        "Gemini",
    ],
    horizontal=True,
)


# Reset if provider changes.

if (
    st.session_state.provider is not None
    and st.session_state.provider != provider
):
    st.session_state.client = None
    st.session_state.store = None
    st.session_state.analysis = None
    st.session_state.indexed_signature = None

st.session_state.provider = provider


# =========================================================
# API KEY
# =========================================================

if provider == "OpenAI":

    st.caption(
        "OpenAI provides the more stable option. "
        "API usage is billed separately from ChatGPT."
    )

    st.link_button(
        "🔑 Create OpenAI API Key",
        "https://platform.openai.com/api-keys",
    )

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
    )

else:

    st.caption(
        "Gemini offers a Free Tier with API rate limits."
    )

    st.link_button(
        "🔑 Create Free Gemini API Key",
        "https://aistudio.google.com/apikey",
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
    )


# =========================================================
# CREATE CLIENT
# =========================================================

if api_key:

    try:

        if provider == "OpenAI":

            st.session_state.client = (
                create_openai_client(
                    api_key
                )
            )

        else:

            st.session_state.client = (
                create_gemini_client(
                    api_key
                )
            )

        st.success(
            f"✅ {provider} API key loaded."
        )

    except Exception as e:

        st.session_state.client = None

        st.error(
            f"{provider} client error: {e}"
        )


# =========================================================
# 2 — UPLOAD
# =========================================================

st.divider()

st.subheader("2. Upload Reports")

optimize_files = st.checkbox(
    "Optimize PDFs before upload",
    value=True,
)

uploaded_files = st.file_uploader(
    "Upload PDF reports",
    type=["pdf"],
    accept_multiple_files=True,
)


if uploaded_files:

    for file in uploaded_files:

        st.write(
            f"📄 {file.name} — "
            f"{format_mb(file.size):.2f} MB"
        )


# =========================================================
# FILE SIGNATURE
# =========================================================

current_signature = None

if uploaded_files:

    current_signature = tuple(
        (
            file.name,
            file.size,
        )
        for file in uploaded_files
    )


if (
    current_signature
    and st.session_state.indexed_signature
    and current_signature
    != st.session_state.indexed_signature
):

    st.session_state.store = None
    st.session_state.analysis = None
    st.session_state.indexed_signature = None


# =========================================================
# PREPARE REPORTS
# =========================================================

prepare = st.button(
    "📚 Prepare Reports",
    type="primary",
    disabled=(
        not api_key
        or not uploaded_files
        or st.session_state.client is None
    ),
)


if prepare:

    status = st.status(
        "Preparing reports...",
        expanded=True,
    )

    temp_paths = []

    try:

        client = st.session_state.client

        # -----------------------------------------
        # CREATE STORE
        # -----------------------------------------

        if provider == "OpenAI":

            status.write(
                "Creating OpenAI Vector Store..."
            )

            store = (
                create_openai_vector_store(
                    client
                )
            )

        else:

            status.write(
                "Creating Gemini File Search Store..."
            )

            store = (
                create_file_search_store(
                    client
                )
            )


        status.write(
            "✅ Document database created."
        )


        # -----------------------------------------
        # PROCESS FILES
        # -----------------------------------------

        progress = st.progress(0)

        total = len(uploaded_files)


        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            status.write(
                f"Processing **{uploaded_file.name}**..."
            )


            # -------------------------------------
            # OPTIMIZE
            # -------------------------------------

            if optimize_files:

                (
                    pdf_path,
                    original_size,
                    optimized_size,
                ) = optimize_pdf(
                    uploaded_file
                )

                temp_paths.append(
                    pdf_path
                )

                if optimized_size < original_size:

                    reduction = (
                        1
                        -
                        (
                            optimized_size
                            / original_size
                        )
                    ) * 100

                    status.write(
                        f"🗜️ "
                        f"{format_mb(original_size):.2f} MB → "
                        f"{format_mb(optimized_size):.2f} MB "
                        f"({reduction:.1f}% smaller)"
                    )

            else:

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                )

                temp.write(
                    uploaded_file.getvalue()
                )

                temp.close()

                pdf_path = temp.name

                temp_paths.append(
                    pdf_path
                )


            # -------------------------------------
            # INDEX
            # -------------------------------------

            status.write(
                f"Indexing **{uploaded_file.name}**..."
            )


            if provider == "OpenAI":

                upload_pdf_to_openai_store(
                    client,
                    store,
                    pdf_path,
                )

            else:

                upload_pdf_path_to_store(
                    client=client,
                    store=store,
                    pdf_path=pdf_path,
                    display_name=uploaded_file.name,
                )


            status.write(
                f"✅ {uploaded_file.name} ready."
            )


            progress.progress(
                int(
                    ((index + 1) / total)
                    * 100
                )
            )


        # -----------------------------------------
        # SESSION
        # -----------------------------------------

        st.session_state.store = store

        st.session_state.indexed_signature = (
            current_signature
        )

        st.session_state.analysis = None

        st.session_state.selected_section = (
            "executive_summary"
        )


        status.update(
            label="✅ Reports ready",
            state="complete",
            expanded=False,
        )


    except Exception as e:

        status.update(
            label="❌ Preparation failed",
            state="error",
        )

        st.error(
            str(e)
        )


    finally:

        for path in temp_paths:

            if (
                path
                and os.path.exists(path)
            ):

                try:
                    os.remove(path)

                except Exception:
                    pass


# =========================================================
# STATUS
# =========================================================

if st.session_state.store is not None:

    st.success(
        f"🟢 {provider} RAG database ready."
    )


# =========================================================
# 3 — MASTER ANALYSIS
# =========================================================

st.divider()

st.subheader(
    "3. Generate Report Intelligence"
)

st.caption(
    "One request generates the dashboard. "
    "Opening dashboard sections uses no additional API calls."
)


analyze_button = st.button(
    "✨ Analyze Reports",
    type="primary",
    use_container_width=True,
    disabled=(
        st.session_state.store is None
    ),
)


if analyze_button:

    try:

        with st.status(
            f"Analyzing with {provider}...",
            expanded=True,
        ) as status:

            status.write(
                "🔎 Retrieving relevant evidence..."
            )


            if provider == "OpenAI":

                analysis = (
                    analyze_openai_reports(
                        st.session_state.client,
                        st.session_state.store,
                    )
                )

            else:

                analysis = (
                    analyze_gemini_reports(
                        st.session_state.client,
                        st.session_state.store,
                    )
                )


            st.session_state.analysis = analysis


            status.update(
                label="✅ Analysis complete",
                state="complete",
                expanded=False,
            )


    except Exception as e:

        error = str(e)

        if "429" in error:

            st.warning(
                f"⏳ {provider} rate limit reached."
            )

        else:

            st.error(
                f"Analysis failed: {error}"
            )


# =========================================================
# 4 — DASHBOARD
# =========================================================

analysis = st.session_state.analysis


if analysis:

    st.divider()

    st.subheader(
        "4. Report Intelligence"
    )


    SECTIONS = {

        "📋 Executive Summary":
            "executive_summary",

        "🌡️ Climate Risks":
            "climate_risks",

        "🌱 Adaptation":
            "adaptation",

        "🏭 Mitigation":
            "mitigation",

        "🎯 Net Zero":
            "net_zero",

        "☁️ Scope 1 / 2 / 3":
            "scope_emissions",

        "📊 Sustainability Targets":
            "sustainability_targets",

        "💧 Water & Drought":
            "water_and_drought",

        "⚡ Energy Transition":
            "energy_transition",

        "🌍 SDG Alignment":
            "sdg_alignment",

    }


    cols = st.columns(3)


    for index, (
        label,
        key
    ) in enumerate(
        SECTIONS.items()
    ):

        with cols[
            index % 3
        ]:

            if st.button(
                label,
                use_container_width=True,
                key=f"section_{key}",
            ):

                st.session_state.selected_section = key


    selected = (
        st.session_state.selected_section
    )


    st.markdown("---")


    section_data = analysis.get(
        selected,
        []
    )


    if isinstance(
        section_data,
        list
    ):

        for item in section_data:

            st.markdown(
                f"- {item}"
            )

    else:

        st.markdown(
            str(section_data)
        )


# =========================================================
# 5 — SUGGESTED QUESTIONS
# =========================================================

if analysis:

    st.divider()

    st.subheader(
        "5. Suggested Questions"
    )


    questions = analysis.get(
        "suggested_questions",
        []
    )


    for question in questions:

        st.markdown(
            f"- {question}"
        )


# =========================================================
# 6 — CUSTOM QUESTION
# =========================================================

if st.session_state.store:

    st.divider()

    st.subheader(
        "6. Ask Your Own Question"
    )

    st.caption(
        "Each custom question uses one additional API request."
    )


    question = st.text_area(
        "Question",
        placeholder=(
            "What are the most important "
            "climate-related financial risks?"
        ),
    )


    if st.button(
        "🔎 Ask",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning(
                "Enter a question first."
            )

        else:

            try:

                with st.spinner(
                    "Searching reports..."
                ):

                    if provider == "OpenAI":

                        answer = (
                            ask_openai_question(
                                st.session_state.client,
                                st.session_state.store,
                                question,
                            )
                        )

                    else:

                        answer = (
                            ask_gemini_question(
                                st.session_state.client,
                                st.session_state.store,
                                question,
                            )
                        )


                st.markdown(
                    "### Answer"
                )

                st.markdown(
                    answer
                )


            except Exception as e:

                st.error(
                    f"Question failed: {e}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    f"Climate Policy Intelligence • {provider}"
)