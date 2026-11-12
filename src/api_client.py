import requests

API_BASE_URL = "http://127.0.0.1:8000"

def check_api_health():
    response = requests.get(
        f"{API_BASE_URL}/health",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def upload_document(file):
    response = requests.post(
        f"{API_BASE_URL}/upload",
        files={
            "file":(
                file.name,
                file.getvalue(),
                "application/pdf",
            )
        },
        timeout=300,
    )

    response.raise_for_status()
    return response.json()

def ask_question(question):
    response = requests.post(
        f"{API_BASE_URL}/ask",
        json={"question":question},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()