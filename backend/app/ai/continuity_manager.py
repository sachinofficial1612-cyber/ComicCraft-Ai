from typing import List, Optional
from ..models.panel import Panel

def build_continuity_context(
    current_panel_num: int,
    all_panels: List[Panel]
) -> str:
    """Extract continuity context from previous and next panels to preserve narrative & visual flow."""
    if not all_panels:
        return ""

    prev_panel = next((p for p in all_panels if p.panel_number == current_panel_num - 1), None)
    next_panel = next((p for p in all_panels if p.panel_number == current_panel_num + 1), None)

    context_parts = []
    if prev_panel:
        context_parts.append(f"Previous panel action: {prev_panel.scene_description or 'Hero advances'}.")
    if next_panel:
        context_parts.append(f"Leading into next panel: {next_panel.scene_description or 'Resolution'}.")

    return " ".join(context_parts)
