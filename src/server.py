#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load .env for local tests (Render ignores this, uses its dashboard vars)
load_dotenv()

SEAM_API_KEY = os.getenv("SEAM_API_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")

# Create server – ONLY name is allowed here!
mcp = FastMCP("Yale Linus Lock Control")

# Print warning if secrets missing (shows in Render logs for debug)
if not SEAM_API_KEY or not DEVICE_ID:
    print("WARNING: Missing SEAM_API_KEY or DEVICE_ID env vars – add them in Render dashboard!")

@mcp.tool()
async def lock_door() -> str:
    """Locks the Yale Linus door."""
    if not SEAM_API_KEY or not DEVICE_ID:
        raise ValueError("SEAM_API_KEY and DEVICE_ID must be set in environment variables.")
    
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
            error = response.json().get("error", {}).get("message", response.text)
        except:
            error = response.text
        raise ValueError(f"Lock failed ({response.status_code}): {error}")

@mcp.tool()
async def unlock_door() -> str:
    """Unlocks the Yale Linus door."""
    if not SEAM_API_KEY or not DEVICE_ID:
        raise ValueError("SEAM_API_KEY and DEVICE_ID must be set in environment variables.")
    
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
            error = response.json().get("error", {}).get("message", response.text)
        except:
            error = response.text
        raise ValueError(f"Unlock failed ({response.status_code}): {error}")

# Keep this unchanged – it's the Render HTTP server setup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting server on {host}:{port}")
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )