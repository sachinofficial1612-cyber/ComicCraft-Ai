from typing import List, Dict, Any

class ComicComposer:
    def calculate_page_layout(self, panel_count: int) -> List[Dict[str, Any]]:
        """
        Determines comic page layout based on panel count.
        4 panels -> 2x2 grid (1 page)
        6 panels -> 2x3 grid (1 page)
        8 panels -> 4 panels per page (2 pages)
        10 panels -> 5 panels per page (2 pages: 3+2 layout)
        """
        if panel_count <= 4:
            return [{"page": 1, "grid": (2, 2), "panels_start": 1, "panels_end": panel_count}]
        elif panel_count == 6:
            return [{"page": 1, "grid": (2, 3), "panels_start": 1, "panels_end": 6}]
        elif panel_count == 8:
            return [
                {"page": 1, "grid": (2, 2), "panels_start": 1, "panels_end": 4},
                {"page": 2, "grid": (2, 2), "panels_start": 5, "panels_end": 8}
            ]
        elif panel_count == 10:
            return [
                {"page": 1, "grid": (2, 3), "panels_start": 1, "panels_end": 6},
                {"page": 2, "grid": (2, 2), "panels_start": 7, "panels_end": 10}
            ]
        else:
            # Default pagination for N panels
            pages = []
            per_page = 4
            p_num = 1
            for idx in range(1, panel_count + 1, per_page):
                end_idx = min(panel_count, idx + per_page - 1)
                pages.append({
                    "page": p_num,
                    "grid": (2, 2),
                    "panels_start": idx,
                    "panels_end": end_idx
                })
                p_num += 1
            return pages

composer = ComicComposer()
