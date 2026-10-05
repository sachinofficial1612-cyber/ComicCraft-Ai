from __future__ import annotations

from typing import Any

import requests


DEFAULT_API_URL = "https://comiccraft-ai-a1rz.onrender.com"


class APIError(Exception):
    """Raised when the ComicCraft backend returns an error."""

    pass


class ComicCraftAPI:
    def __init__(
        self,
        base_url: str = DEFAULT_API_URL,
        timeout: int = 600,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # ============================================================
    # INTERNAL REQUEST METHOD
    # ============================================================

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """
        Send an HTTP request to the ComicCraft backend.
        """

        kwargs.setdefault(
            "timeout",
            self.timeout,
        )

        url = (
            f"{self.base_url}/"
            f"{path.lstrip('/')}"
        )

        try:

            response = requests.request(
                method=method,
                url=url,
                **kwargs,
            )

        except requests.Timeout as exc:

            raise APIError(
                "The backend request timed out. "
                "The Render server may still be generating "
                "your comic. Please try again after waiting "
                "a little while."
            ) from exc

        except requests.ConnectionError as exc:

            raise APIError(
                "Could not connect to the ComicCraft backend. "
                "Please check that the Render backend is running."
            ) from exc

        except requests.RequestException as exc:

            raise APIError(
                f"Could not connect to backend: {exc}"
            ) from exc

        # --------------------------------------------------------
        # HTTP ERROR
        # --------------------------------------------------------

        if not response.ok:

            try:

                data = response.json()

                if isinstance(
                    data,
                    dict,
                ):

                    detail = data.get(
                        "detail"
                    )

                    error = data.get(
                        "error"
                    )

                    message = data.get(
                        "message"
                    )

                    if detail:
                        error_message = detail

                    elif error:
                        error_message = error

                    elif message:
                        error_message = message

                    else:
                        error_message = str(
                            data
                        )

                else:

                    error_message = str(
                        data
                    )

            except ValueError:

                error_message = (
                    response.text.strip()
                    or f"HTTP {response.status_code}"
                )

            raise APIError(
                f"Backend error "
                f"({response.status_code}): "
                f"{error_message}"
            )

        # --------------------------------------------------------
        # EMPTY RESPONSE
        # --------------------------------------------------------

        if not response.content:

            return None

        # --------------------------------------------------------
        # JSON RESPONSE
        # --------------------------------------------------------

        content_type = (
            response.headers
            .get(
                "content-type",
                "",
            )
            .lower()
        )

        if "application/json" in content_type:

            try:

                return response.json()

            except ValueError as exc:

                raise APIError(
                    "Backend returned invalid JSON."
                ) from exc

        # --------------------------------------------------------
        # FILE / BINARY RESPONSE
        # --------------------------------------------------------

        return response.content

    # ============================================================
    # HEALTH
    # ============================================================

    def health(self):
        return self._request(
            "GET",
            "/api/health",
        )

    def ai_health(self):
        return self._request(
            "GET",
            "/api/health/ai",
        )

    # ============================================================
    # PROJECTS
    # ============================================================

    def create_project(
        self,
        title: str,
        story: str,
        style: str,
        panel_count: int | str,
    ):
        """
        Create a new ComicCraft project.

        Backend expects:

            original_prompt: string
            story: string
            style: string
            panel_count: string
        """

        payload = {
            "original_prompt": str(
                title
            ).strip(),

            "story": str(
                story
            ).strip(),

            "style": str(
                style
            ).strip(),

            "panel_count": str(
                panel_count
            ),
        }

        return self._request(
            "POST",
            "/api/projects",
            json=payload,
        )

    def list_projects(self):

        return self._request(
            "GET",
            "/api/projects",
        )

    def get_project(
        self,
        project_id,
    ):

        return self._request(
            "GET",
            f"/api/projects/{project_id}",
        )

    # ============================================================
    # COMIC GENERATION
    # ============================================================

    def generate_comic(
        self,
        project_id,
    ):
        """
        Start comic generation.
        """

        return self._request(
            "POST",
            f"/api/projects/{project_id}/generate",
        )

    def get_project_status(
        self,
        project_id,
    ):
        """
        Get the current comic generation status.
        """

        return self._request(
            "GET",
            f"/api/projects/{project_id}/status",
        )

    # ============================================================
    # PROJECT UPDATE
    # ============================================================

    def update_project(
        self,
        project_id,
        updates,
    ):

        return self._request(
            "PUT",
            f"/api/projects/{project_id}",
            json=updates,
        )

    def delete_project(
        self,
        project_id,
    ):

        return self._request(
            "DELETE",
            f"/api/projects/{project_id}",
        )

    # ============================================================
    # PANELS
    # ============================================================

    def update_panel(
        self,
        project_id,
        panel_id,
        updates,
    ):

        return self._request(
            "PUT",
            f"/api/projects/"
            f"{project_id}/panels/"
            f"{panel_id}",
            json=updates,
        )

    def regenerate_panel_image(
        self,
        project_id,
        panel_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/panels/"
            f"{panel_id}/regenerate-image",
        )

    def regenerate_panel_story(
        self,
        project_id,
        panel_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/panels/"
            f"{panel_id}/regenerate-story",
        )

    def regenerate_panel_both(
        self,
        project_id,
        panel_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/panels/"
            f"{panel_id}/regenerate-both",
        )

    def delete_panel(
        self,
        project_id,
        panel_id,
    ):

        return self._request(
            "DELETE",
            f"/api/projects/"
            f"{project_id}/panels/"
            f"{panel_id}",
        )

    def add_panel(
        self,
        project_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/panels",
        )

    # ============================================================
    # EXPORT
    # ============================================================

    def export_pdf(
        self,
        project_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/export/pdf",
        )

    def export_png(
        self,
        project_id,
    ):

        return self._request(
            "POST",
            f"/api/projects/"
            f"{project_id}/export/png",
        )