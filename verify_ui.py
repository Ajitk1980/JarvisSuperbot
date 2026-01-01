import os
import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting browser verification...")
    with sync_playwright() as p:
        browsers = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit
        }
        
        for name, browser_type in browsers.items():
            print(f"\nTrying to launch {name}...")
            try:
                # Basic args that work for most
                browser = browser_type.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage'] if name == "chromium" else []
                )
                print(f"{name} launched successfully.")
                
                context = browser.new_context(viewport={'width': 1280, 'height': 720})
                page = context.new_page()
                
                print("Navigating to app...")
                page.goto("http://localhost:8501", timeout=30000)
                
                print("Waiting for page load...")
                page.wait_for_selector("div.stApp", state="attached", timeout=10000)
                
                print("Page loaded. Waiting 5s for styles...")
                time.sleep(5)
                
                output_path = f"/home/kajit/JarvisSuperbot/ui_proof_{name}.png"
                print(f"Taking screenshot to {output_path}...")
                page.screenshot(path=output_path)
                
                browser.close()
                print(f"Verification successful with {name}!")
                return # Exit on first success
                
            except Exception as e:
                print(f"Failed with {name}: {e}")
                
    print("\nAll browsers failed.")

if __name__ == "__main__":
    run()
