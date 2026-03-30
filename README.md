# FastAPI & Streamlit Photo/Video Sharing App

A production-ready full-stack web application demonstrating advanced backend concepts using **FastAPI** and a dynamic frontend built with **Streamlit**. 

This project goes beyond the basics, implementing robust features like JWT-based user authentication, database integration, Pydantic data validation, and third-party media handling via ImageKit.

## 🚀 Features

* **RESTful API Setup:** Built with FastAPI, utilizing path parameters, query parameters, and robust request body handling.
* **Data Validation:** Strict type hinting and payload validation using Pydantic models.
* **Database Integration:** Full CRUD (Create, Read, Update, Delete) operations connected to a persistent database.
* **Authentication & Authorization:** Secure user login utilizing JWT (JSON Web Tokens) to protect specific endpoints.
* **Media Uploads:** Integrated with ImageKit for seamless image and video uploading and retrieval.
* **Error Handling:** Custom exception handling and appropriate HTTP status codes.
* **Interactive Frontend:** A streamlined, responsive UI built with Streamlit to interact with the FastAPI backend.
* **Auto-generated Docs:** Interactive Swagger UI documentation provided out-of-the-box by FastAPI.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **Frontend:** Streamlit
* **Data Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens)
* **Media Storage:** ImageKit API
* **Package Manager:** uv
* **Database:** SQLite

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:
* Python 3.8+ installed
* An [ImageKit.io](https://imagekit.io/) account and API keys
* `uv` installed for dependency management (`pip install uv`)

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/FastAPIPhotoVideoSharing.git](https://github.com/ADHAN-Z/FASTAPI-Image-and-Video-Sharing-Platform)
cd FASTAPI-Image-and-Video-Sharing-Platform
```

**2. Install Dependencies
This project uses uv for lightning-fast dependency management.
```bash
# Create a virtual environment and sync dependencies
uv sync
```

**3. Environment Variables
Create a .env file in the root directory and add your secret keys:
```bash
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_URL=your_url
```

**🏃‍♂️ Running the Application
You will need two terminal windows to run the backend and frontend simultaneously. Ensure your virtual environment is activated in both.

*Terminal 1: Start the FastAPI Backend
```bash
uvicorn main:app --reload
```

*Terminal 2: Start the Streamlit Frontend
```bash
streamlit run frontend.py
```

**📂 Project Structure
```
├── app/                   # Backend application module
│   ├── app.py             # Core app logic / routers
│   ├── db.py              # Database connection and session management
│   ├── images.py          # ImageKit integration and media routes
│   ├── schemas.py         # Pydantic models for data validation
│   └── users.py           # User authentication and management
├── .env                   # Environment variables (Ignored in Git)
├── frontend.py            # Streamlit frontend application
├── main.py                # FastAPI application entry point
├── pyproject.toml         # Project dependencies and metadata
├── uv.lock                # Lockfile for the uv package manager
└── README.md              # Project documentation
```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
