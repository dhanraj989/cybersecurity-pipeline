# **Cybersecurity Pipeline**
A **fully automated cybersecurity scanning pipeline** built with **LangChain, Groq API, and Streamlit**. 
This system dynamically executes **security scans** using **Nmap and FFUF**, enforces scope restrictions, and generates AI-powered insights.

---

## **1. System Architecture**
The cybersecurity pipeline follows a **modular design** with the following key components:

### **a) `security_pipeline.py` (Backend)**
- Manages **task execution** for security scans.
- Supports **Nmap (port scanning)** and **FFUF (web fuzzing)**.
- Stores scan results in a **SQLite database** (`security_scans.db`).
- Integrates **Groq AI** for security analysis.
- Implements **scope enforcement** to prevent unauthorized scans.

### **b) `dashboard.py` (Frontend - Streamlit UI)**
- Provides an **interactive web interface** for launching security scans.
- Allows users to **input target domains** and **select security tools**.
- Displays **real-time scan logs and AI-generated security insights**.
- Supports **exporting reports** as **JSON**.
- Provides an **option to clear previous scan history**.

### **c) Database (`security_scans.db`)**
- Stores **scan execution logs**, including:
  - Target domain/IP.
  - Security tool used.
  - Command executed.
  - Scan status (Completed, Failed).
  - Scan output.
  - Timestamp.

---

## **2. Agent Roles & Responsibilities**
The system operates **agentically**, breaking down security tasks into **executables** and adapting dynamically.

### **Agentic Workflow**
1. **Receives User Input**:  
   - Takes **target URL/IP** and **selected tools**.
2. **Enforces Scope**:  
   - Blocks scans on unauthorized domains.
3. **Breaks Down Task Execution**:  
   - Runs **Nmap** for **port scanning**.
   - Runs **FFUF** for **web fuzzing**.
4. **Executes Scans**:  
   - Runs tools as **subprocesses**.
   - Logs outputs to **SQLite**.
5. **Analyzes Results using AI (Groq API)**:  
   - AI extracts **potential vulnerabilities**.
   - AI provides **recommendations & next steps**.
6. **Stores & Displays Data**:  
   - Results are stored in `security_scans.db`.
   - UI displays results in **Streamlit Dashboard**.
7. **Report Generation**:  
   - Allows users to **download JSON reports**.

---

## **3. Scope Enforcement Strategy**
To ensure **ethical and controlled scanning**, the pipeline enforces **target scope restrictions**:

### **Scope Rules**
✅ **Allowed Targets:**  
   - Only scans **user-defined domains/IPs**.  
   - Rejects unauthorized scans.

✅ **Auto-Blocking Mechanism:**  
   - If a scan attempts to run outside the defined scope, it **terminates execution**.

✅ **HTTPS Enforcement:**  
   - Converts **HTTP URLs to HTTPS** automatically.
   - Ensures correct **subdomain resolution**.

✅ **Input Sanitization:**  
   - Removes unwanted characters.
   - Prevents **command injection attacks**.

---

## **4. Steps to Install & Run the Project**
### **1️⃣ Install Dependencies**
#### **Using Poetry (Recommended)**
```bash
poetry install
poetry shell # leave this line if it is causing error
```
#### **Or Using `pip`**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **2️⃣ Install Required Security Tools**  
Before running scans, **install Nmap & FFUF** manually:

#### **Installing Nmap**
- **Windows:** Download & install from [Nmap Official Site](https://nmap.org/download.html)
- **Linux/macOS:** Install using:
  ```bash
  sudo apt install nmap  # Debian/Ubuntu
  brew install nmap  # macOS (Homebrew)
  ```

#### **Installing FFUF**
- **Windows:** Download from [FFUF GitHub Releases](https://github.com/ffuf/ffuf/releases)
- **Linux/macOS:** Install using:
  ```bash
  go install github.com/ffuf/ffuf@latest
  ```

### **3️⃣ Set Environment Variables**
```bash
export GROQ_API_KEY="your-groq-api-key"
```
*(For Windows, use `set GROQ_API_KEY="your-groq-api-key"` in CMD.)*

### **4️⃣ Run the Streamlit UI**
```bash
streamlit run dashboard.py
```

### **5️⃣ Select Target & Tools**
- Enter **Target Domain/IP**.
- Select **Nmap** (port scan) and/or **FFUF** (web fuzzing).
- Click **🔍 Start Scan**.

### **6️⃣ View Results & AI Insights**
- View **real-time scan logs**.
- Check **AI-generated security insights**.
- **Download** results as a JSON file.

### **7️⃣ Clear Scan History (Optional)**
Click **🧹 Clear Scan History** to remove all stored scan data.

---

## **5. Features & Technologies**
🔹 **Automated Security Scans** → Runs **Nmap & FFUF** for reconnaissance.  
🔹 **Scope Enforcement** → Ensures ethical scanning.  
🔹 **AI-Powered Analysis** → Uses **Groq LLM** for vulnerability insights.  
🔹 **Database Logging** → Stores scan results in **SQLite**.  
🔹 **Streamlit UI** → Easy-to-use **dashboard interface**.  
🔹 **JSON Reports** → **Downloadable scan logs** for further analysis.  
🔹 **Poetry Dependency Management** → Easy to install & manage libraries.

---

## **6. Project Files**
| File | Description |
|------|------------|
| `security_pipeline.py` | Executes security scans, enforces scope, integrates AI. |
| `dashboard.py` | Streamlit UI for launching & viewing security scans. |
| `security_scans.db` | SQLite database storing scan results. |
| `pyproject.toml` | Poetry configuration for dependencies. |
| `security_scan.log` | Error logging |

---

## **7. Future Enhancements**
🚀 **Support for more security tools** (e.g., SQLmap, Nikto).  
🚀 **Integration with external databases** (e.g., PostgreSQL).  
🚀 **Scheduled automated scans**.  
🚀 **Multi-user authentication for security**.

---
### **🔹 Developed by Dhanraj Malla | Powered by LangChain, Groq AI & Streamlit 🚀**

---

## **8. How to Execute the Cybersecurity Pipeline**
Once everything is installed, follow these steps to **execute security scans**:

### **Step 1: Start the Streamlit Dashboard**
Run the following command in your terminal to launch the **Streamlit UI**:
```bash
streamlit run dashboard.py
```
This will open a **web dashboard** where you can enter targets and select security tools.

### **Step 2: Perform a Security Scan**
1. **Enter the target domain/IP** (e.g., `example.com` or `192.168.1.1`).
2. **Select the security tools** you want to use (`Nmap`, `FFUF`).
3. **Click on** `🔍 Start Scan`.
4. Wait for the scans to **complete**, and results will be displayed.

### **Step 3: Download Reports (Optional)**
- After scans are completed, you can **download the scan report as JSON** by clicking **📥 Download JSON Report**.

### **Step 4: View Previous Scans**
- Check past scans under **📂 Previous Scan Logs**.
- If you want to **clear all scan history**, click **🧹 Clear Scan History**.

---
