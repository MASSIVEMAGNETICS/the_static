from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:5175")

    # 1. Create a custom node.
    page.get_by_placeholder("Describe the AI task...").fill("My test prompt")
    page.get_by_role("button", name="Create").click()

    # 2. Find the newly created node and double-click it.
    node_to_edit = page.locator(".canvas div:has-text('Custom Node: My test prompt...')")
    expect(node_to_edit).to_be_visible()
    node_to_edit.dblclick()

    # 3. The modal should appear. Find it and its textarea.
    modal = page.locator(".modal-content")
    expect(modal).to_be_visible()
    expect(modal.locator("h2")).to_have_text("Edit Custom Node Prompt")

    # 4. Edit the prompt text.
    modal_textarea = modal.locator("textarea")
    expect(modal_textarea).to_have_value("My test prompt") # Verify initial value
    modal_textarea.fill("This is the new, edited prompt.")

    # 5. Save the changes.
    modal.get_by_role("button", name="Save").click()

    # 6. The modal should disappear.
    expect(modal).not_to_be_visible()

    # 7. Verify the node on the canvas has the updated prompt text.
    expect(node_to_edit.locator("div.bg-gray-100")).to_have_text("This is the new, edited prompt.")

    # 8. Take a screenshot.
    page.screenshot(path="jules-scratch/verification/verification.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
