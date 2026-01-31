#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load .env file for local testing (Render uses dashboard env vars instead)
load_dotenv()

# Get secrets from environment
SEAM_API_KEY = os.getenv("SEAM_API_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")

# Create the MCP server
mcp = FastMCP(
    name="Yale Linus Lock Control",
    version="1.0.0",
    description="Lock and unlock your Yale Linus smart lock using Seam API"
)

# Optional: Warn if secrets are missing (helps debugging)
if not SEAM_API_KEY or not DEVICE_ID:
    print("WARNING: SEAM_API_KEY and/or DEVICE_ID are not set. Tools will fail until you add them in Render dashboard.")

@mcp.tool()
async def lock_door() -> str:
    """Locks the Yale Linus door."""
    if not SEAM_API_KEY or not DEVICE_ID:
        raise ValueError("SEAM_API_KEY and DEVICE_ID must be configured in environment variables.")
    
    url = "https://connect.getseam.com/locks/lock_door"
    headers = {
        "Authorization": f"Bearer {SEAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"device_id": DEVICE_ID}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in (200, 201):
        return "Door locked successfully."
    else:
        try:
            error_msg = response.json().get("error", {}).get("message", response.text)
        except:
            error_msg = response.text
        raise ValueError(f"Lock failed: {response.status_code} - {error_msg}")

@mcp.tool()
async def unlock_door() -> str:
    """Unlocks the Yale Linus door."""
    if not SEAM_API_KEY or not DEVICE_ID:
        raise ValueError("SEAM_API_KEY and DEVICE_ID must be configured in environment variables.")
    
    url = "https://connect.getseam.com/locks/unlock_door"
    headers = {
        "Authorization": f"Bearer {SEAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"device_id": DEVICE_ID}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in (200, 201):
        return "Door unlocked successfully."
    else:
        try:
            error_msg = response.json().get("error", {}).get("message", response.text)
        except:
            error_msg = response.text
        raise ValueError(f"Unlock failed: {response.status_code} - {error_msg}")

# ────────────────────────────────────────────────
# Do NOT change anything below this line
# This is what makes the server run on Render / Heroku / Vercel etc.
# ────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting MCP server on {host}:{port}")
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )