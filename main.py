from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import uvicorn

app = FastAPI()

@app.get("/redfin")
async def get_redfin_estimate(address: str = Query(...)):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            search_url = f"https://www.redfin.com/stingray/do/location-autocomplete?location={address}"
            await page.goto(search_url)
            content = await page.content()

            # Close browser
            await browser.close()

            # Simulate successful parse for now
            return JSONResponse(content={"address": address, "redfin_estimate": "Success (placeholder)"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)