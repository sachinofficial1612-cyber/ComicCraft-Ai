import os
import time
import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_full_user_flow():
    print("--- 1. Testing Health Endpoint ---")
    resp = httpx.get(f"{BASE_URL}/api/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    print(f"Health Response: {resp.json()}")

    print("\n--- 2. Creating New Project ('Free the Fox') ---")
    create_payload = {
        "original_prompt": "A brave red fox named Free explores an enchanted forest, discovering glowing ancient ruins.",
        "character_name": "Free",
        "setting": "Enchanted Forest",
        "tone": "Dramatic",
        "art_style": "Realistic",
        "panel_count": "6"
    }
    proj_resp = httpx.post(f"{BASE_URL}/api/projects", json=create_payload)
    assert proj_resp.status_code == 201, f"Create project failed: {proj_resp.text}"
    project = proj_resp.json()
    project_id = project["id"]
    print(f"Created Project ID: {project_id}, Title: {project['title']}")

    print("\n--- 3. Running AI Generation Pipeline ---")
    gen_resp = httpx.post(f"{BASE_URL}/api/projects/{project_id}/generate")
    assert gen_resp.status_code == 200, f"Generate pipeline failed: {gen_resp.text}"
    gen_project = gen_resp.json()
    assert gen_project["status"] == "completed", f"Status expected 'completed', got '{gen_project['status']}'"
    print(f"Pipeline completed with {len(gen_project['panels'])} panels and {len(gen_project['characters'])} characters.")

    print("\n--- 4. Verifying Character Bible ---")
    for char in gen_project["characters"]:
        print(f"Character: {char['name']} | Appearance: {char['appearance']}")

    print("\n--- 5. Verifying Panel Artwork & Dialogue Overlay ---")
    panels = gen_project["panels"]
    assert len(panels) == 6
    for p in panels:
        print(f"Panel #{p['panel_number']} | Title: {p['title']} | Narration: {p['narration']}")
        assert p["status"] == "completed"

    print("\n--- 6. Editing Panel #2 Dialogue ---")
    panel_2 = panels[1]
    update_payload = {
        "narration": "A strange blue light illuminates the mossy path.",
        "dialogue": [{"speaker": "Free", "text": "This moss is glowing with magic!", "bubble_type": "speech"}]
    }
    update_resp = httpx.put(f"{BASE_URL}/api/projects/{project_id}/panels/{panel_2['id']}", json=update_payload)
    assert update_resp.status_code == 200
    print(f"Updated Panel #2: {update_resp.json()['narration']}")

    print("\n--- 7. Regenerating Panel #2 Image ---")
    regen_resp = httpx.post(f"{BASE_URL}/api/projects/{project_id}/panels/{panel_2['id']}/regenerate-image")
    assert regen_resp.status_code == 200
    print("Regenerated Panel #2 image successfully.")

    print("\n--- 8. Testing PDF Export ---")
    pdf_resp = httpx.post(f"{BASE_URL}/api/projects/{project_id}/export/pdf")
    assert pdf_resp.status_code == 200
    pdf_info = pdf_resp.json()
    print(f"PDF Exported: {pdf_info['filename']} -> Download URL: {pdf_info['download_url']}")

    print("\n--- 9. Testing PNG Export ---")
    png_resp = httpx.post(f"{BASE_URL}/api/projects/{project_id}/export/png")
    assert png_resp.status_code == 200
    png_info = png_resp.json()
    print(f"PNG Pages Exported: {len(png_info['pages'])} pages.")

    print("\n--- 10. Verifying Download PDF File Endpoint ---")
    dl_resp = httpx.get(f"{BASE_URL}{pdf_info['download_url']}")
    assert dl_resp.status_code == 200
    assert len(dl_resp.content) > 1000
    print(f"Downloaded PDF File Byte Size: {len(dl_resp.content)} bytes.")

    print("\n[SUCCESS] ALL 10 END-TO-END VERIFICATION STEPS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_full_user_flow()
