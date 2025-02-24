import os
import subprocess
import logging
import sqlite3
from typing import List, Dict
from datetime import datetime
from groq import Groq  # Import Groq API

# Setup logging
logging.basicConfig(filename="security_scan.log", level=logging.INFO)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Groq API key not found! Set GROQ_API_KEY in environment variables.")

client = Groq(api_key=GROQ_API_KEY)

# Database setup
DB_NAME = "security_scans.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            tool TEXT,
            command TEXT,
            status TEXT,
            output TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Function to sanitize target URLs (Fixes "www." and ensures "https://")
def sanitize_target_url(target: str) -> str:
    target = target.strip().lower()

    if target.startswith("http://"):
        target = target.replace("http://", "https://")  # Convert HTTP to HTTPS

    if not target.startswith("https://"):
        target = "https://" + target  # Ensure it starts with HTTPS

    target = target.replace("www.", "")  # Remove "www."
    return target

# Define a class for security tasks
class SecurityTask:
    def __init__(self, command: str, description: str, target: str, tool: str):
        self.command = command
        self.description = description
        self.status = "Pending"
        self.output = None
        self.target = target
        self.tool = tool

    def execute(self) -> str:
        logging.info(f"Executing task: {self.description} -> {self.command}")
        try:
            result = subprocess.run(self.command, shell=True, capture_output=True, text=True, timeout=60)
            self.output = result.stdout.strip()
            self.status = "Completed" if result.returncode == 0 else "Failed"

            if result.stderr:
                logging.error(f"Error running {self.tool}: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.output = "Timeout Error: Scan took too long!"
            self.status = "Failed"
            logging.error(f"Timeout: {self.command} took too long to execute.")
        except Exception as e:
            self.output = str(e)
            self.status = "Error"
            logging.error(f"Execution failed: {e}")

        # Save to database
        self.save_to_db()
        return self.output

    def save_to_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scans (target, tool, command, status, output)
            VALUES (?, ?, ?, ?, ?)
        """, (self.target, self.tool, self.command, self.status, self.output))
        conn.commit()
        conn.close()

def clean_target(target: str) -> str:
    """Convert https://example.com to example.com (for Nmap)"""
    return target.replace("https://", "").replace("http://", "").strip()

# Ensure wordlist exists for FFUF
DEFAULT_WORDLIST = os.path.join(os.getcwd(), "wordlists", "dirb", "common.txt")

if not os.path.exists(DEFAULT_WORDLIST):
    os.makedirs(os.path.dirname(DEFAULT_WORDLIST), exist_ok=True)
    print("Downloading default wordlist...")
    os.system(f"curl -o {DEFAULT_WORDLIST} https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt")

# Updated Tools (Removed wfuzz)
TOOLS = {
    "nmap": "nmap -Pn -sV -T4 -F {target}",
    "ffuf": f'ffuf -u {{target}}/FUZZ -w "{DEFAULT_WORDLIST}"'
}

def generate_tasks(target: str, tools: List[str]) -> List[SecurityTask]:
    clean_target_value = clean_target(target)  # Nmap needs "example.com"
    sanitized_target = sanitize_target_url(target)  # FFUF needs "https://example.com"

    return [
        SecurityTask(
            command=TOOLS[tool].format(target=clean_target_value if tool == "nmap" else sanitized_target),
            description=f"Run {tool} on {sanitized_target}",
            target=sanitized_target,
            tool=tool
        )
        for tool in tools if tool in TOOLS
    ]

# Enforce scope restrictions
def enforce_scope(target: str, allowed_scope: List[str]) -> bool:
    return any(target.endswith(scope) for scope in allowed_scope)

# Run Groq LLM for security insights
def run_groq_agent(target: str, tools: List[str], scan_results: Dict[str, str]) -> str:
    # Format scan results for better analysis
    formatted_results = "\n".join([f"{task}: {output}" for task, output in scan_results.items()])

    prompt = f"""
    You are a cybersecurity assistant. You have been provided with real security scan results
    for the target: {target}. Analyze these results and provide structured, actionable insights.

    Scan Results:
    {formatted_results}

    Please summarize:
    - Potential security vulnerabilities based on scan findings.
    - Recommendations for securing the system.
    - Any follow-up scans that may be needed.
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content  # ✅ Now, Groq will analyze actual scan data!

# Run security scan workflow
def run_security_pipeline(target: str, tools: List[str], allowed_scope: List[str]):
    if not enforce_scope(target, allowed_scope):
        return {"error": f"Target {target} is out of scope"}

    tasks = generate_tasks(target, tools)
    scan_results = {task.description: task.execute() for task in tasks}

    # ✅ Pass scan results to Groq for analysis
    groq_analysis = run_groq_agent(target, tools, scan_results)

    return {"groq_analysis": groq_analysis, "scan_results": scan_results}