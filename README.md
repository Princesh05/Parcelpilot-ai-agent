# 🚚 ParcelPilot AI Agent

An AI-powered logistics customer-support agent that combines **LLM-based reasoning, tool calling, RAG, structured workflows, access control, and human confirmation** to handle parcel-management requests.

---

## 📌 Overview

**ParcelPilot AI Agent** is an intelligent customer-support system designed for logistics and shipment-management scenarios.

The system allows users to interact with an AI agent through a web interface. The agent can understand customer requests, retrieve relevant order or ticket information, search operational policies and agreements, prepare sensitive actions, and request confirmation before executing those actions.

The project demonstrates a practical **agentic AI architecture** rather than a simple chatbot.

---

## ✨ Key Features

### 🤖 AI Agent

The ParcelPilot agent understands user requests and determines which tools or workflows are required.

It supports tasks such as:

* Order status lookup
* Ticket lookup
* Cancellation requests
* Escalation requests
* Policy-related questions
* Customer agreement checks
* Tool selection and execution
* Confirmation-based actions

---

### 🔧 Tool Calling

The agent can interact with structured backend tools instead of generating answers only from the LLM.

The project contains dedicated tool modules for:

* Data operations
* Action operations
* Document operations
* Tool dispatching

Sensitive operations are separated from simple read-only operations.

---

### 📚 RAG-Based Knowledge Retrieval

ParcelPilot includes a Retrieval-Augmented Generation (RAG) pipeline for retrieving information from operational documents.

The knowledge base includes:

* Current support policy
* Deprecated support policy
* Cancellation and service-credit SOP
* Product operations guide
* Known issues
* Enterprise agreements

The retrieved information can be used by the agent when answering policy and customer-agreement questions.

---

### 🔐 Access Control

The system includes access-control logic to ensure that users can only access information they are authorized to access.

This is especially important for customer-specific logistics information.

---

### ⚠️ Human-in-the-Loop Confirmation

Sensitive operations are not immediately executed.

For example:

```text
User
 ↓
Cancellation Request
 ↓
Agent prepares cancellation
 ↓
Confirmation required
 ↓
User confirms
 ↓
Cancellation executed
```

This prevents accidental execution of sensitive operations.

The same approach is used for escalation workflows.

---

### 🚨 Escalation Workflow

The agent can prepare escalation tickets when a shipment issue requires additional support.

For example:

```text
Shipment was picked up
        ↓
Status still shows BOOKED
        ↓
Agent identifies escalation requirement
        ↓
Escalation prepared
        ↓
User confirmation
        ↓
Escalation created
```

---

## 🏗️ System Architecture

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Web Frontend   │
                         │     ui.py        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │     main.py      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Agent Layer    │
                         │    agent.py      │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          ┌────────────┐   ┌────────────┐   ┌────────────┐
          │ Data Tools │   │Action Tools│   │  Document  │
          │            │   │            │   │   Tools    │
          └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
                │                │                │
                ▼                ▼                ▼
          ┌────────────┐   ┌────────────┐   ┌────────────┐
          │   Data     │   │ Confirmation│   │    RAG     │
          │  Service   │   │   Layer     │   │ Retriever  │
          └────────────┘   └────────────┘   └─────┬──────┘
                                                  │
                                                  ▼
                                           ┌─────────────┐
                                           │ Chroma DB   │
                                           └─────────────┘
```

---

## 📂 Project Structure

```text
parcelpilot-ai-agent/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── tool_schemas.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── data/
│   │   ├── access_control.py
│   │   ├── loader.py
│   │   └── service.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── metadata.py
│   │   └── retriever.py
│   │
│   ├── tools/
│   │   ├── action_tools.py
│   │   ├── data_tools.py
│   │   ├── document_tools.py
│   │   └── tool_dispatcher.py
│   │
│   ├── config.py
│   ├── main.py
│   └── ui.py
│
├── chroma_db/
│   └── chroma.sqlite3
│
├── data/
│   ├── escalations.json
│   ├── ParcelPilot_Assessment_Data.xlsx
│   └── documents/
│       ├── 01_Support_Policy_v3_CURRENT.pdf
│       ├── 02_Support_Policy_v2_DEPRECATED.pdf
│       ├── 03_Cancellation_and_Service_Credit_SOP_v4.pdf
│       ├── 04_Product_Operations_Guide_and_Known_Issues.pdf
│       ├── 05_Northstar_Logistics_Enterprise_Agreement.pdf
│       └── 06_LumenWorks_Service_Agreement.pdf
│
├── tests/
│   ├── test_access_control.py
│   ├── test_actions.py
│   ├── test_action_tools.py
│   ├── test_agent.py
│   ├── test_agent_chat.py
│   ├── test_agent_security.py
│   ├── test_api.py
│   ├── test_confirmation.py
│   ├── test_data_service.py
│   ├── test_dispatcher.py
│   ├── test_document_tools.py
│   ├── test_escalation.py
│   ├── test_retriever.py
│   ├── test_tools.py
│   └── test_tool_edge_cases.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* REST API

### AI / Agent

* Large Language Model (LLM)
* Gemini API
* Agentic tool calling
* Structured tool execution
* Human-in-the-loop confirmation

### RAG

* Retrieval-Augmented Generation
* ChromaDB
* Document ingestion
* Metadata-based retrieval

### Data

* JSON
* Excel
* PDF documents

### Testing

* Pytest
* Unit tests
* Integration tests
* Agent workflow tests
* Security and access-control tests

### Frontend

* Python-based UI
* FastAPI integration
* Chat interface

---

## 📚 Knowledge Base

The RAG knowledge base contains the following documents:

| Document                          | Purpose                                    |
| --------------------------------- | ------------------------------------------ |
| Support Policy v3                 | Current support policies                   |
| Support Policy v2                 | Deprecated policy reference                |
| Cancellation & Service Credit SOP | Cancellation and service-credit procedures |
| Product Operations Guide          | Product operations and known issues        |
| Northstar Logistics Agreement     | Enterprise customer agreement              |
| LumenWorks Service Agreement      | Enterprise customer agreement              |

The system is designed to prefer the appropriate/current information when answering policy-related questions.

---

## 🔄 Example Workflows

### 1. Order Status Lookup

```text
User:
What is the current status of order ORD-1001?

        ↓

Agent identifies order ID

        ↓

lookup_order

        ↓

Data Service

        ↓

Order information

        ↓

Agent response
```

---

### 2. Cancellation

```text
User:
I want to cancel order ORD-1001.

        ↓

Agent identifies cancellation intent

        ↓

prepare_cancellation

        ↓

Confirmation required

        ↓

User confirms

        ↓

Cancellation action executed
```

---

### 3. Cancellation Rejection

```text
User:
I want to cancel order ORD-1001.

        ↓

Cancellation prepared

        ↓

Confirmation requested

        ↓

User rejects

        ↓

Action is NOT executed
```

---

### 4. Escalation

```text
User:
Please escalate ticket TKT-504.
The shipment was picked up but still shows BOOKED.

        ↓

Agent identifies escalation requirement

        ↓

prepare_escalation

        ↓

Confirmation requested

        ↓

User confirms

        ↓

Escalation created
```

---

### 5. Policy Question

```text
User asks about cancellation policy

        ↓

Agent identifies knowledge requirement

        ↓

RAG Retriever

        ↓

ChromaDB

        ↓

Relevant policy documents

        ↓

Agent generates answer
```

---

## 🔐 Security

ParcelPilot includes multiple safety mechanisms:

* Access-control checks
* Customer-context validation
* Confirmation before sensitive actions
* Separation of read-only and write operations
* Structured tool execution
* Environment-variable based API configuration

API keys and secrets should never be committed to the repository.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd parcelpilot-ai-agent
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root and configure the required API credentials.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

**Never commit `.env` or API keys to GitHub.**

---

## ▶️ Running the Application

From the project root:

```bash
uvicorn app.main:app --reload
```

The FastAPI server will start locally.

Open:

```text
http://127.0.0.1:8000
```

---

## 🧪 Running Tests

Run the complete test suite:

```bash
pytest -q
```

The project includes tests covering:

* Agent behavior
* Tool execution
* Action workflows
* Confirmation flows
* Escalation
* Document retrieval
* Access control
* Security
* API endpoints
* Edge cases

### Current Test Status

The core test suite has been extensively tested.

Some agent-chat tests depend on the external Gemini API and may fail when the configured Gemini project reaches its API quota. Such failures appear as:

```text
429 RESOURCE_EXHAUSTED
```

This is an external API quota limitation rather than a local application exception.

---

## 🚀 Future Improvements

Possible production-level improvements include:

* Persistent production database
* Authentication and authorization
* Real-time carrier API integration
* Conversation memory
* Better observability and monitoring
* Docker deployment
* CI/CD pipeline
* Cloud deployment
* Multi-agent orchestration
* Production-grade rate-limit handling
* Automated evaluation of agent responses

---

## 🎯 Project Objective

The objective of ParcelPilot is to demonstrate how an AI agent can move beyond simple question answering and perform structured, goal-oriented tasks using external tools and knowledge sources.

The project combines:

**LLM + Agent + Tool Calling + RAG + APIs + Security + Human Confirmation**

to create a practical AI-powered logistics customer-support system.

---

## 👨‍💻 Author

**Prince Kumar Sharma**

B.Tech — Computer Science & Engineering
Specialization — Artificial Intelligence & Machine Learning

---

## 📄 License

This project was developed for educational and assessment purposes.
