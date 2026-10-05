from __future__ import annotations

from typing import Any

import streamlit as st

from api_client import APIError, ComicCraftAPI


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ComicCraft AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_BACKEND = "https://comiccraft-ai-a1rz.onrender.com"

STYLES = [
    "Manga",
    "Comic Book",
    "Cartoon",
    "Anime",
    "Watercolor",
    "Cyberpunk",
    "Fantasy",
    "Noir",
]

PANEL_OPTIONS = [4, 6, 8, 10, 12]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(124, 58, 237, 0.18),
                    transparent 35%
                ),
                #0f172a;
        }

        .title {
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .subtitle {
            color: #cbd5e1;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        .hero {
            padding: 2rem;
            border-radius: 22px;
            background:
                linear-gradient(
                    135deg,
                    rgba(124, 58, 237, 0.2),
                    rgba(30, 41, 59, 0.9)
                );
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "backend_url" not in st.session_state:
    st.session_state.backend_url = DEFAULT_BACKEND

if "project" not in st.session_state:
    st.session_state.project = None


# ============================================================
# API CLIENT
# ============================================================

@st.cache_resource
def get_api(url: str) -> ComicCraftAPI:
    return ComicCraftAPI(url)


api = get_api(st.session_state.backend_url)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_project_id(project: Any) -> str | None:
    """Return project ID from a backend project response."""

    if not isinstance(project, dict):
        return None

    project_id = project.get("id")

    if project_id is None:
        project_id = project.get("project_id")

    if project_id is None:
        return None

    return str(project_id)


def get_panels(project: Any) -> list[dict]:
    """Return the project's panels safely."""

    if not isinstance(project, dict):
        return []

    panels = project.get("panels", [])

    if isinstance(panels, list):
        return [
            panel
            for panel in panels
            if isinstance(panel, dict)
        ]

    return []


def build_url(value: Any) -> str | None:
    """Convert backend relative URLs into absolute URLs."""

    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    if value.startswith("http://"):
        return value

    if value.startswith("https://"):
        return value

    if value.startswith("/"):
        return (
            st.session_state.backend_url.rstrip("/")
            + value
        )

    return value


def image_url(panel: dict) -> str | None:
    """Find an artwork URL from a panel."""

    possible_keys = [
        "image_url",
        "artwork_url",
        "image",
        "artwork",
        "image_path",
        "artwork_path",
    ]

    for key in possible_keys:
        value = panel.get(key)
        url = build_url(value)

        if url:
            return url

    return None


def refresh_project() -> bool:
    """Refresh current project from backend."""

    project_id = get_project_id(
        st.session_state.project
    )

    if not project_id:
        return False

    try:
        st.session_state.project = api.get_project(
            project_id
        )
        return True

    except APIError as exc:
        st.error(
            f"Could not refresh project: {exc}"
        )
        return False


def status_text(project: dict) -> str:
    """Return readable project status."""

    value = project.get(
        "status",
        project.get(
            "generation_status",
            "unknown",
        ),
    )

    return str(value)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎨 ComicCraft AI")

    st.caption(
        "AI-powered comic story and artwork generator"
    )

    backend_input = st.text_input(
        "FastAPI backend URL",
        value=st.session_state.backend_url,
    ).strip()

    if (
        backend_input
        and backend_input
        != st.session_state.backend_url
    ):

        st.session_state.backend_url = (
            backend_input.rstrip("/")
        )

        get_api.clear()

        api = get_api(
            st.session_state.backend_url
        )

    if st.button(
        "🔌 Test Backend",
        use_container_width=True,
    ):

        try:
            result = api.health()

            if isinstance(result, dict):

                backend_status = result.get(
                    "status",
                    "OK",
                )

                st.success(
                    f"Backend: {backend_status}"
                )

            else:
                st.success(
                    "Backend is reachable."
                )

        except APIError as exc:
            st.error(str(exc))

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "✨ Create Comic",
            "📖 My Comic",
            "🧩 Panels",
            "📤 Export",
        ],
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🎨 ComicCraft AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Turn your story idea into a complete illustrated comic."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# CREATE COMIC
# ============================================================

if page == "✨ Create Comic":

    st.markdown(
        '<div class="hero">',
        unsafe_allow_html=True,
    )

    st.markdown("## ✨ Create a New Comic")

    st.write(
        "Describe your story, choose an art style, "
        "and create your comic project."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    with st.form("create_comic_form"):

        title = st.text_input(
            "Comic title",
            placeholder="The Quest of Elena",
        )

        story = st.text_area(
            "Story idea",
            height=220,
            placeholder=(
                "Elena discovers an ancient map "
                "and follows it into a forgotten "
                "magical forest..."
            ),
        )

        col1, col2 = st.columns(2)

        with col1:
            style = st.selectbox(
                "Art style",
                STYLES,
            )

        with col2:
            panel_count = st.selectbox(
                "Number of panels",
                PANEL_OPTIONS,
                index=1,
            )

        submitted = st.form_submit_button(
            "🚀 Create Comic",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not title.strip():

            st.error(
                "Please enter a comic title."
            )

        elif not story.strip():

            st.error(
                "Please enter a story."
            )

        else:

            try:

                with st.spinner(
                    "Creating comic project..."
                ):

                    project = api.create_project(
                        title=title.strip(),
                        story=story.strip(),
                        style=style,
                        panel_count=panel_count,
                    )

                st.session_state.project = project

                st.success(
                    "✅ Comic project created successfully!"
                )

                st.info(
                    "Open **📖 My Comic** and click "
                    "**🚀 Generate Complete Comic**."
                )

            except APIError as exc:

                st.error(
                    f"❌ {exc}"
                )


# ============================================================
# MY COMIC
# ============================================================

elif page == "📖 My Comic":

    project = st.session_state.project

    if not project:

        st.info(
            "No comic project exists yet."
        )

        st.write(
            "Go to **✨ Create Comic** to create one."
        )

    else:

        project_id = get_project_id(project)

        if not project_id:

            st.error(
                "The backend response does not contain "
                "a valid project ID."
            )

        else:

            title = project.get(
                "title",
                "My Comic",
            )

            st.header(
                f"📖 {title}"
            )

            story = project.get(
                "story",
                project.get(
                    "original_prompt",
                    "",
                ),
            )

            if story:
                st.write(story)

            panels = get_panels(project)

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Panels",
                len(panels),
            )

            col2.metric(
                "Style",
                project.get(
                    "style",
                    "Unknown",
                ),
            )

            col3.metric(
                "Status",
                status_text(project),
            )

            st.divider()

            # ====================================================
            # GENERATE COMIC
            # ====================================================

            if st.button(
                "🚀 Generate Complete Comic",
                type="primary",
                use_container_width=True,
            ):

                try:

                    with st.spinner(
                        "🎨 Generating your comic... "
                        "This may take several minutes."
                    ):

                        result = api.generate_comic(
                            project_id
                        )

                    if isinstance(result, dict):

                        st.session_state.project = (
                            result
                        )

                    st.success(
                        "🎉 Comic generation request completed!"
                    )

                    refresh_project()

                    st.rerun()

                except APIError as exc:

                    st.error(
                        f"❌ Comic generation failed:\n\n{exc}"
                    )

                except Exception as exc:

                    st.error(
                        f"❌ Unexpected error:\n\n{exc}"
                    )

            # ====================================================
            # REFRESH
            # ====================================================

            if st.button(
                "🔄 Refresh Project",
                use_container_width=True,
            ):

                if refresh_project():
                    st.success(
                        "Project refreshed."
                    )
                    st.rerun()

            # ====================================================
            # PANELS
            # ====================================================

            st.divider()

            st.subheader(
                "🖼️ Comic Panels"
            )

            current_project = (
                st.session_state.project
            )

            current_panels = get_panels(
                current_project
            )

            if not current_panels:

                st.info(
                    "No panels have been generated yet."
                )

            else:

                for index, panel in enumerate(
                    current_panels,
                    start=1,
                ):

                    with st.container(
                        border=True
                    ):

                        panel_number = panel.get(
                            "panel_number",
                            index,
                        )

                        st.markdown(
                            f"### Panel {panel_number}"
                        )

                        col1, col2 = st.columns(
                            [1.1, 1]
                        )

                        with col1:

                            url = image_url(panel)

                            if url:

                                try:

                                    st.image(
                                        url,
                                        use_container_width=True,
                                    )

                                except Exception:

                                    st.warning(
                                        "Unable to load artwork."
                                    )

                            else:

                                st.info(
                                    "Artwork is not available yet."
                                )

                        with col2:

                            narration = panel.get(
                                "narration",
                                panel.get(
                                    "caption",
                                    "",
                                ),
                            )

                            dialogue = panel.get(
                                "dialogue",
                                "",
                            )

                            if narration:

                                st.markdown(
                                    "**Narration**"
                                )

                                st.write(
                                    narration
                                )

                            if dialogue:

                                st.markdown(
                                    "**Dialogue**"
                                )

                                st.write(
                                    dialogue
                                )

                            st.caption(
                                "Status: "
                                + str(
                                    panel.get(
                                        "status",
                                        "unknown",
                                    )
                                )
                            )


# ============================================================
# PANEL EDITOR
# ============================================================

elif page == "🧩 Panels":

    project = st.session_state.project

    if not project:

        st.info(
            "Create a comic first."
        )

    else:

        project_id = get_project_id(project)

        if not project_id:

            st.error(
                "Project ID not found."
            )

        else:

            st.header(
                "🧩 Panel Editor"
            )

            panels = get_panels(project)

            if not panels:

                st.info(
                    "No panels available."
                )

            else:

                for index, panel in enumerate(
                    panels,
                    start=1,
                ):

                    panel_id = panel.get(
                        "id",
                        panel.get(
                            "panel_id"
                        ),
                    )

                    if panel_id is None:
                        continue

                    panel_id = str(panel_id)

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            f"Panel "
                            f"{panel.get('panel_number', index)}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            url = image_url(panel)

                            if url:

                                st.image(
                                    url,
                                    use_container_width=True,
                                )

                            else:

                                st.info(
                                    "No artwork available."
                                )

                        with col2:

                            narration = st.text_area(
                                "Narration",
                                value=(
                                    panel.get(
                                        "narration",
                                        panel.get(
                                            "caption",
                                            "",
                                        ),
                                    )
                                    or ""
                                ),
                                key=(
                                    f"narration_{panel_id}"
                                ),
                            )

                            dialogue = st.text_area(
                                "Dialogue",
                                value=(
                                    panel.get(
                                        "dialogue",
                                        "",
                                    )
                                    or ""
                                ),
                                key=(
                                    f"dialogue_{panel_id}"
                                ),
                            )

                            col_a, col_b, col_c = (
                                st.columns(3)
                            )

                            with col_a:

                                if st.button(
                                    "💾 Save",
                                    key=(
                                        f"save_{panel_id}"
                                    ),
                                    use_container_width=True,
                                ):

                                    try:

                                        api.update_panel(
                                            project_id,
                                            panel_id,
                                            {
                                                "narration": (
                                                    narration
                                                ),
                                                "dialogue": (
                                                    dialogue
                                                ),
                                            },
                                        )

                                        refresh_project()

                                        st.success(
                                            "Panel saved."
                                        )

                                    except APIError as exc:

                                        st.error(
                                            str(exc)
                                        )

                            with col_b:

                                if st.button(
                                    "🎨 Image",
                                    key=(
                                        f"image_{panel_id}"
                                    ),
                                    use_container_width=True,
                                ):

                                    try:

                                        with st.spinner(
                                            "Regenerating image..."
                                        ):

                                            api.regenerate_panel_image(
                                                project_id,
                                                panel_id,
                                            )

                                        refresh_project()

                                        st.success(
                                            "Image regenerated."
                                        )

                                        st.rerun()

                                    except APIError as exc:

                                        st.error(
                                            str(exc)
                                        )

                            with col_c:

                                if st.button(
                                    "✍️ Story",
                                    key=(
                                        f"story_{panel_id}"
                                    ),
                                    use_container_width=True,
                                ):

                                    try:

                                        with st.spinner(
                                            "Regenerating story..."
                                        ):

                                            api.regenerate_panel_story(
                                                project_id,
                                                panel_id,
                                            )

                                        refresh_project()

                                        st.success(
                                            "Story regenerated."
                                        )

                                        st.rerun()

                                    except APIError as exc:

                                        st.error(
                                            str(exc)
                                        )

                st.divider()

                if st.button(
                    "➕ Add Panel",
                    use_container_width=True,
                ):

                    try:

                        with st.spinner(
                            "Adding panel..."
                        ):

                            api.add_panel(
                                project_id
                            )

                        refresh_project()

                        st.success(
                            "Panel added."
                        )

                        st.rerun()

                    except APIError as exc:

                        st.error(
                            str(exc)
                        )


# ============================================================
# EXPORT
# ============================================================

elif page == "📤 Export":

    project = st.session_state.project

    if not project:

        st.info(
            "Create a comic first."
        )

    else:

        project_id = get_project_id(project)

        if not project_id:

            st.error(
                "Project ID not found."
            )

        else:

            st.header(
                "📤 Export Comic"
            )

            col1, col2 = st.columns(2)

            # ====================================================
            # PDF
            # ====================================================

            with col1:

                st.subheader(
                    "📕 PDF"
                )

                if st.button(
                    "Generate PDF",
                    use_container_width=True,
                ):

                    try:

                        with st.spinner(
                            "Creating PDF..."
                        ):

                            result = api.export_pdf(
                                project_id
                            )

                        if not isinstance(
                            result,
                            dict,
                        ):

                            st.warning(
                                "Backend did not return PDF information."
                            )

                        else:

                            url = build_url(
                                result.get(
                                    "download_url"
                                )
                            )

                            if url:

                                st.link_button(
                                    "⬇️ Open / Download PDF",
                                    url,
                                    use_container_width=True,
                                )

                            else:

                                st.warning(
                                    "No PDF download URL was returned."
                                )

                    except APIError as exc:

                        st.error(
                            f"❌ PDF export failed:\n\n{exc}"
                        )

                    except Exception as exc:

                        st.error(
                            f"❌ Unexpected PDF error:\n\n{exc}"
                        )

            # ====================================================
            # PNG
            # ====================================================

            with col2:

                st.subheader(
                    "🖼️ PNG"
                )

                if st.button(
                    "Generate PNG",
                    use_container_width=True,
                ):

                    try:

                        with st.spinner(
                            "Creating PNG files..."
                        ):

                            result = api.export_png(
                                project_id
                            )

                        if not isinstance(
                            result,
                            dict,
                        ):

                            st.warning(
                                "Backend did not return PNG information."
                            )

                        else:

                            pages = result.get(
                                "pages",
                                [],
                            )

                            if not pages:

                                st.warning(
                                    "No PNG pages were returned."
                                )

                            else:

                                for index, item in enumerate(
                                    pages,
                                    start=1,
                                ):

                                    if not isinstance(
                                        item,
                                        dict,
                                    ):
                                        continue

                                    url = build_url(
                                        item.get(
                                            "download_url"
                                        )
                                    )

                                    filename = item.get(
                                        "filename",
                                        f"comic-page-{index}.png",
                                    )

                                    if url:

                                        st.link_button(
                                            f"⬇️ {filename}",
                                            url,
                                            use_container_width=True,
                                        )

                    except APIError as exc:

                        st.error(
                            f"❌ PNG export failed:\n\n{exc}"
                        )

                    except Exception as exc:

                        st.error(
                            f"❌ Unexpected PNG error:\n\n{exc}"
                        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ComicCraft AI • Streamlit • FastAPI • Gemini"
)