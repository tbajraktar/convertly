from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import re

router = APIRouter()

class TerminalRequest(BaseModel):
    query: str
    os_type: str = "linux" # or "windows"

class TerminalResponse(BaseModel):
    command: str
    explanation: str
    risk_level: str # "safe", "medium", "high"

@router.post("/api/terminal-helper", response_model=TerminalResponse)
async def generate_command(request: TerminalRequest):
    query = request.query.lower()
    os_type = request.os_type.lower()
    
    command = ""
    explanation = ""
    risk_level = "safe"

    # Simple Heuristics for MVP (Simulate AI)
    
    # 1. Listing Files
    if "list" in query or "show files" in query or "what's here" in query:
        if "all" in query or "hidden" in query:
            command = "ls -la" if os_type != "windows" else "dir /a"
            explanation = "Lists all files, including hidden ones."
        else:
            command = "ls" if os_type != "windows" else "dir"
            explanation = "Lists files in the current directory."
            
    # 2. Moving/Renaming
    elif "move" in query or "rename" in query:
        command = "mv [source] [destination]" if os_type != "windows" else "move [source] [destination]"
        explanation = "Moves or renames files. Replace [brackets] with actual filenames."
        risk_level = "medium"

    # 3. Copying
    elif "copy" in query:
        if "folder" in query or "directory" in query:
            command = "cp -r [source] [dest]" if os_type != "windows" else "xcopy [source] [dest] /E /I"
            explanation = "Copies a directory recursively."
        else:
            command = "cp [source] [dest]" if os_type != "windows" else "copy [source] [dest]"
            explanation = "Copies a file."
            
    # 4. Deleting (High Risk)
    elif "delete" in query or "remove" in query or "wipe" in query:
        risk_level = "high"
        if "folder" in query or "directory" in query:
            command = "rm -rf [directory]" if os_type != "windows" else "rmdir /s /q [directory]"
            explanation = "⚠️ DELETES a directory and everything inside it forever. Be careful!"
        else:
            command = "rm [file]" if os_type != "windows" else "del [file]"
            explanation = "Deletes a specific file."

    # 5. Network / IP
    elif "ip" in query or "address" in query:
        command = "ip addr" if os_type == "linux" else ("ifconfig" if os_type == "mac" else "ipconfig")
        explanation = "Shows network interface information and IP addresses."
        
    # 6. Grep / Search Text
    elif "find text" in query or "search for" in query:
        command = "grep -r '[text]' ." if os_type != "windows" else "findstr /s '[text]' *"
        explanation = "Searches for text inside files recursively."

    # 7. Fallback / AI Placeholder
    else:
        command = "# AI implementation pending for complex queries"
        explanation = "I didn't understand that specific request yet. Try simpler commands like 'list files' or 'delete folder'."
        risk_level = "safe"

    return TerminalResponse(
        command=command,
        explanation=explanation,
        risk_level=risk_level
    )
