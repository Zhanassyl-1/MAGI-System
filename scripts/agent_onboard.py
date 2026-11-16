#!/usr/bin/env python3
"""
MAGI-System Agent Onboarding & Verification Script
Verifies environment, reads required protocols, and asserts role boundaries.
"""

import argparse
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ROLE_CONFIG = {
    "fe-1": {
        "title": "Frontend Lead / UI Architecture",
        "team": "Frontend",
        "doc": "FRONTEND.md",
        "responsibilities": [
            "UI/UX Architecture, responsive grid, styling tokens",
            "App routing and shared state structures",
            "Coordinate component specifications with FE-2 and API contracts with FE-3"
        ]
    },
    "fe-2": {
        "title": "Frontend Components Specialist",
        "team": "Frontend",
        "doc": "FRONTEND.md",
        "responsibilities": [
            "Reusable atomic components and UI elements",
            "CSS/Styling conformity and layout implementation",
            "Component unit tests and story/mock verification"
        ]
    },
    "fe-3": {
        "title": "Frontend Integration Specialist",
        "team": "Frontend",
        "doc": "FRONTEND.md",
        "responsibilities": [
            "API client integration and HTTP handling",
            "Form management, validation, and optimistic updates",
            "End-to-end frontend state sync with backend endpoints"
        ]
    },
    "be-1": {
        "title": "Backend Lead / API Architecture",
        "team": "Backend",
        "doc": "BACKEND.md",
        "responsibilities": [
            "API routing architecture and schema contracts (OpenAPI/GraphQL)",
            "Data model design, ORM mappings, and migrations",
            "Core server middleware and error handling standards"
        ]
    },
    "be-2": {
        "title": "Backend Services Specialist",
        "team": "Backend",
        "doc": "BACKEND.md",
        "responsibilities": [
            "Business logic layer and domain services implementation",
            "Third-party integrations and event handlers",
            "Background jobs, caching, and data processing"
        ]
    },
    "be-3": {
        "title": "Backend Security & Database Specialist",
        "team": "Backend",
        "doc": "BACKEND.md",
        "responsibilities": [
            "Authentication, authorization, and session management",
            "Database query optimization, indexing, and connection pools",
            "Input sanitization, rate limiting, and security compliance"
        ]
    },
    "qa-1": {
        "title": "QA Lead / Test Architecture",
        "team": "QA",
        "doc": "QA.md",
        "responsibilities": [
            "Test strategy, CI test automation pipeline, coverage standards",
            "E2E test framework configuration and environment sanity",
            "Final gatekeeper review and merge approval for Pull Requests"
        ]
    },
    "qa-2": {
        "title": "QA Frontend Specialist",
        "team": "QA",
        "doc": "QA.md",
        "responsibilities": [
            "Frontend component testing and accessibility (a11y) checks",
            "Cross-browser and viewport UI validation",
            "Visual regression and client-side error boundary verification"
        ]
    },
    "qa-3": {
        "title": "QA Backend & Integration Specialist",
        "team": "QA",
        "doc": "QA.md",
        "responsibilities": [
            "API contract tests, status code and payload validation",
            "Security vulnerability audits and negative testing",
            "Performance sanity, database integrity, and concurrency tests"
        ]
    },
    "pm": {
        "title": "Project Manager / MAGI Coordinator",
        "team": "Management",
        "doc": "MANAGER.md",
        "responsibilities": [
            "Decompose user requests into atomic tasks",
            "Maintain dependency graphs and ensure no deadlocks",
            "Track progress, resolve bottlenecks, and audit task board"
        ]
    }
}

REQUIRED_GLOBAL_DOCS = [
    "CONTRIBUTING.md",
    "AGENTS.md",
    "TASKS.md",
    "PROJECT_PLAN.md"
]


def check_docs(role_key: str):
    missing = []
    for doc in REQUIRED_GLOBAL_DOCS:
        path = os.path.join(REPO_ROOT, doc)
        if not os.path.exists(path):
            missing.append(doc)
            
    role_info = ROLE_CONFIG[role_key]
    role_doc = os.path.join(REPO_ROOT, role_info["doc"])
    if not os.path.exists(role_doc):
        missing.append(role_info["doc"])
        
    return missing


def main():
    parser = argparse.ArgumentParser(description="MAGI Agent Onboarding Protocol")
    parser.add_argument("--agent", required=True, help="Agent identifier (e.g. FE-1, BE-2, QA-3, PM)")
    args = parser.parse_args()
    
    agent_key = args.agent.lower()
    if agent_key not in ROLE_CONFIG:
        print(f"[FATAL] Invalid Agent ID: {args.agent}. Recognized IDs: {list(ROLE_CONFIG.keys())}", file=sys.stderr)
        sys.exit(1)
        
    info = ROLE_CONFIG[agent_key]
    print("=" * 70)
    print(f" MAGI-SYSTEM AGENT ONBOARDING: {args.agent.upper()} ({info['title']})")
    print("=" * 70)
    print(f"Team:            {info['team']}")
    print(f"Team Protocol:   {info['doc']}")
    print("\nPrimary Responsibilities:")
    for r in info["responsibilities"]:
        print(f"  • {r}")
        
    print("\nMandatory Reading Checklist:")
    for doc in REQUIRED_GLOBAL_DOCS:
        print(f"  [✓] {doc}")
    print(f"  [✓] {info['doc']}")
    
    missing = check_docs(agent_key)
    if missing:
        print(f"\n[WARNING] The following instruction files are missing from repository: {missing}")
    else:
        print("\nAll protocol documents verified in repository.")
        
    print("\nCRITICAL OPERATIONAL RULES:")
    print(" 1. GitHub is single source of truth. Zero shared memory across agent processes.")
    print(" 2. Never commit directly to 'main'. Always work on your designated task branch.")
    print(" 3. Run 'python3 scripts/magi.py next --agent {0}' to find and claim work.".format(args.agent.upper()))
    print(" 4. All changes must go through a Pull Request with complete verification evidence.")
    print(" 5. QA Team sign-off is required before merging any PR.")
    print("=" * 70)


if __name__ == "__main__":
    main()
