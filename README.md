# OrchestrAI - A Multi-Agent System based on LangGraph (In-progress)

<img width="2120" height="1188" alt="RAG model" src="https://github.com/user-attachments/assets/036ea65a-4752-4b8f-adbe-848476f0cd39" />



OrchestrAI is a modular, agent-based orchestration system built using LangGraph, designed to coordinate complex AI workflows across specialized agents such as Coders, Researchers, Generalists, and RAG-based retrieval systems. A Supervisor agent ensures quality control, providing final validation before any output is sent to the user.

📌 Project Overview

This system implements a multi-agent architecture with the following core components:
  - Orchestrator: Acts as the central brain of the system. It analyzes the current state of the workflow, chooses the next best agent to handle the task, and justifies every routing decision.
  - Supervisor: Validates the full reasoning trace, checks logical consistency, efficiency, and completeness of the output, and ensures only high-quality responses reach the user.
  - Agents:
    
    -> 🧠 General Agent – Handles general-purpose tool access like calendar updates, flight lookups, email, and Google Maps.
    
    -> 🔍 Researcher Agent – Performs structured fact-finding from sources like Wikipedia, PubMed, and Arxiv.
    
    -> 🧑‍💻 Coding Agent – Implements, debugs, or computes results using Python scripts, functions, or code snippets.
    
    -> 📚 RAG Agent – Responsible for retrieval-augmented generation when queries are related to uploaded files or internal knowledge sources.
    
The entire workflow is implemented using LangGraph's graph-based execution model, allowing fine-grained control over execution flow, branching, loops, and task redirection.

Flow Summary:
1. User provides a query or request.

2. Orchestrator evaluates the task and routes it to the appropriate agent (general, coder, researcher, or rag) based on task complexity and scope.

3. Agents process the task and return outputs.

4. Orchestrator composes a structured reasoning trace and sends it to the Supervisor.

5. Supervisor validates the entire reasoning path:

  - If correct → Sends final output to the user.

  - If incorrect/incomplete → Loops back to the Orchestrator for revision.

Reach out to me for any queries!
