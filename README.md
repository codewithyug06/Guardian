# Guardian | Strategic Risk Intelligence
**Autonomous. Behavioral. Predictive. Self-Healing.**

---

## 🚩 The Problem Statement
### "The Compliance Velocity Gap"

**Formal Statement:** Global financial regulations (like PCI-DSS, GDPR, and DPDPA) change faster than human teams can read them. Traditional compliance tools are reactive—they only alert you *after* a violation has occurred and the fine is imminent.

**The "Human" Reality (Example):** A Compliance Officer cannot physically read 500+ pages of regulatory updates daily while simultaneously monitoring thousands of server logs for data leaks. This manual bottleneck leads to **"Compliance Drift,"** where a bank’s security posture slowly degrades until a catastrophic fine occurs.

---

## 🛡️ The Utility: What is Guardian Used For?
Guardian is used to turn Compliance from a "Checklist" into an **"Autonomous Immune System."**

It is specifically designed for:

* **🚫 Preventing Fines Before They Happen:** Instead of just logging a violation, it uses **Self-Healing AI** to write and deploy code patches (like encryption) instantly.

* **👀 Omni-Channel Surveillance:** It monitors data leaks that humans miss, such as a credit card number visible in a screenshot (**Vision AI**) or a risky verbal order given on a recorded call (**Audio AI**).

* **⚖️ Automated Legal Reasoning:** It is used to autonomously draft legal policy amendments when new laws are passed, keeping the organization's rulebook up to date without expensive legal consultants.

* **🔒 Trust & Auditing:** It is used to prove compliance to external auditors using **Immutable Crypto-Hashing**, ensuring that no one tampered with the security logs.

---


## 🚀 Extraordinary Innovations

### 1. 👯 The Mirror Node (Digital Twin Simulation)
Before any AI-generated code patch touches production, the **Mirror Agent** simulates it in a virtual banking environment. It evaluates the patch for **Latency Delta**, **CPU Load**, and **Transaction Success Rate** to ensure remediation does not negatively impact performance or cause downtime.

### 2. 🔐 Immutable Decision Vault (Trust Anchor)
Guardian provides a mathematically tamper-proof audit trail by hashing every critical decision (Risk Detection → Patch Generation → Swarm Consensus) into a **SHA-256 Merkle Root**. This ensures that compliance logs cannot be edited or spoofed by human administrators, providing a "Trust Anchor" for external auditors.

### 3. 🦎 "The Chameleon" (Context-Aware Defense)
The system features an adaptive defense posture that dynamically adjusts **Isolation Forest** anomaly detection thresholds. When the **Prophet Agent** forecasts a rising risk trend, the **Sentry Agent** automatically tightens its behavioral analysis sensitivity without manual intervention.

### 4. 🚚 Supply Chain Guardian
Compliance monitoring extends beyond the internal firewall. Guardian proactively scans public security advisories for 3rd-party vendors (e.g., AWS, Stripe, Auth0) to identify systemic risks originating from the supply chain before they impact the core banking infrastructure.

### 5. 📜 Autonomous Policy Legislator
When regulatory updates are discovered, the **Architect Agent** doesn't just report the gap; it autonomously drafts specific legal amendments for the bank's internal policy documents, ensuring governance evolves at the speed of law.

---

## 🧠 The Swarm Architecture (Multi-Agent Logic)

The ecosystem is orchestrated via a cyclic graph of specialized AI Agents using **LangGraph**:

| Agent Node | Role | Capability |
| :--- | :--- | :--- |
| **🕵️ Scout** | **Discovery** | Scans for regulatory updates using **"Deep Proof" Chain-of-Verification (CoVe)** to eliminate hallucinations. |
| **💀 Ghost** | **Stress-test** | Acts as an internal **Red Team**, simulating adversarial attacks (SQLi, Velocity Floods) to validate defenses. |
| **🌐 Federated** | **Collaboration** | Connects to a federated risk ledger to pull decentralized threat intelligence from peer institutions. |
| **👁️ Sentry** | **Monitoring** | Multi-modal surveillance: **Vision AI** for dashboards, **Audio AI** for calls, and **ML** for behavioral log analysis. |
| **🏗️ Architect** | **Strategy** | Maps gaps to **Financial Liability ($)** and autonomously drafts policy evolution amendments. |
| **💻 Coder** | **Remediation** | Generates "Self-Healing" Python patches (e.g., AES-256 Tokenization) to fix detected compliance holes. |
| **🪞 Mirror** | **Simulation** | Executes the **Digital Twin** simulation to verify patch safety and performance impact. |
| **🤝 Consensus** | **Auditing** | Performs swarm peer-review of all patches and locks decisions into the **Immutable Hash Vault**. |
| **🔮 Prophet** | **Forecasting** | Predicts 30-day systemic risk trajectories to drive the system’s adaptive sensitivity. |
| **⛔ Visa Guard** | **Enforcement** | Enterprise-grade **Kill-Switch** that blocks non-compliant transactions in "Safe Mode" pending human review. |

---

## 💻 Technology Stack

* **Orchestration**: `LangGraph` & `StateGraph` for decentralized multi-agent coordination.
* **Core Intelligence**: `OpenAI GPT-4o` for semantic legal reasoning and code generation.
* **Retrieval Logic**: **Hybrid Mesh RAG** combining `ChromaDB` (Vector Search) and `NetworkX` (Structured Knowledge Graphs).
* **Machine Learning**: `Scikit-learn` (Isolation Forest) for behavioral anomaly detection.
* **Predictive Modeling**: `Prophet-style` temporal analysis for 30-day risk forecasting.
* **Interface**: `Streamlit` with a custom "Neon-Glass" UI and interactive `Plotly` telemetry.
* **Trust Layer**: `SHA-256` Merkle Hashing for immutable audit trails.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.9+
* OpenAI API Key

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/guardian.git](https://github.com/your-username/guardian.git)
    cd guardian
    ```

2.  **Environment Configuration**
    Create a `.env` file in the root directory and add your API credentials:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Command Center**
    ```bash
    streamlit run app.py
    ```

---

## 🛠️ Project Flow (The Sense-Evolve-Repair Loop)

1.  **Sense**: The **Scout** and **Sentry** nodes continuously monitor global laws and multi-modal data streams for potential violations.
2.  **Verify**: The **CoVe** engine triple-checks findings against official texts and case law to ensure 100% accuracy.
3.  **Evaluate**: The **Architect** quantifies the risk into a financial liability metric.
4.  **Simulate**: The **Coder** generates a patch, which is immediately tested by the **Mirror** node in a digital twin simulation.
5.  **Audit**: The **Consensus** swarm verifies the fix and anchors it with an immutable hash.
6.  **Enforce**: The **Visa Guard** node executes the fix or triggers a kill-switch if a critical threat is detected.

---

## 🕹️ Dashboard Features
* **Glassmorphism UI**: A futuristic Command Center aesthetic with animated real-time alerts.
* **Neural Mesh**: A visual knowledge graph showing how global regulations semantically link together.
* **Risk Trajectory**: Interactive Plotly charts visualizing the projected 30-day risk curve.
* **Native Swarm Chat**: A natural-language interface to query the swarm's reasoning or request remediation details.

---

## 📂 Project Structure

```text
guardian/
├── app.py                 # "Command Center" Dashboard (UI/UX)
├── internal_policy.txt    # Ingested knowledge for the RAG pipeline
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (OpenAI API Keys)
└── core/
    ├── agents.py          # Swarm node definitions (Scout, Ghost, Mirror, etc.)
    ├── graph.py           # LangGraph orchestration and workflow logic
    ├── state.py           # Swarm-wide state management (TypedDict)
    └── tools.py           # Capability layer (ML, Hashing, Simulations, Search)
```
---
## 📖 Executive Summary
**Guardian** is an autonomous, agentic AI platform designed to solve **Problem Statement 4: Continuous PCI/PII Compliance**. 

Unlike passive dashboards, Guardian is a **Self-Healing Organism**. It leverages a decentralized **Multi-Agent Swarm** to transition from passive monitoring to proactive, self-healing assurance. It autonomously discovers regulatory shifts, maps them to internal policies, detects multi-modal violations (Vision/Audio/Logs), and executes edge-level enforcement to neutralize financial liability in real-time.

---

