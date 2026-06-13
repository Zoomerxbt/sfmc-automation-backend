# sfmc-automation-backend

A robust backend boilerplate built with **FastAPI** designed to handle authentication with the **Salesforce Marketing Cloud (SFMC) REST API**. 

This project solves the foundational hurdle of developing SFMC Custom Apps (such as custom Journey Builder activities or CloudPages integrations) by securely managing the OAuth2 Client Credentials flow, fetching access tokens, and caching them efficiently.

---

## 🚀 The Vision: Upcoming Features
This repository serves as the foundation for a suite of SFMC utility apps. The immediate next feature on the roadmap is an **Email Annotation Injection Tool**. 

> **Roadmap Feature:** This upcoming tool will allow developers to inject custom JSON-LD metadata into SFMC email templates, enabling rich features like Google Promotions tab highlights, deal badges, and expiration dates directly from an external interface.

---

## ✨ Features

* **FastAPI Core:** High-performance, asynchronous Python backend with automatic OpenAPI/Swagger documentation.
* **SFMC OAuth2 Integration:** Implements the Server-to-Server Client Credentials flow to retrieve access tokens from the `/v1/token` endpoint.
* **Token Life-Cycle Management:** (Optional/Planned) Logic to cache and reuse tokens until expiration to avoid hitting SFMC rate limits.
* **Extensible Blueprint:** Clean architecture designed to easily plug in custom routing for future SFMC application features.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **HTTP Client:** HTTPX (Asynchronous HTTP requests)
* **ASGI Server:** Uvicorn

---

## 📋 Prerequisites

Before running the application, you need an **Installed Package** in Salesforce Marketing Cloud:
1. Log in to SFMC and navigate to **Administration > Setup > Platform Tools > Apps > Installed Packages**.
2. Click **New**, give it a name, and save.
3. Click **Add Component** and select **API Integration**.
4. Choose **Server-to-Server** integration.
5. Grant the necessary scopes (e.g., `Automation: Read/Write` or `Email: Read/Write` depending on your eventual custom app needs).
6. Copy your **Client ID**, **Client Secret**, and **Authentication Base URI**.

---

## ⚙️ Setup & Installation
