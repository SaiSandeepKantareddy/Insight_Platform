# import subprocess

# def summarize_with_ollama(text: str, model="llama3") -> str:
#     prompt = f"Summarize the following text in 3 bullet points:\n{text}"
#     result = subprocess.run([
#         "ollama", "run", model, prompt
#     ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#     if result.returncode == 0:
#         return result.stdout.strip()
#     else:
#         raise RuntimeError(f"Ollama error: {result.stderr}")

import requests

# def summarize_with_ollama(input_text: str, model: str = "llama3") -> str:
#     api_url = "http://ollama:11434/api/generate"
#     payload = {
#         "model": model,
#         "prompt": input_text
#     }
#     headers = {"Content-Type": "application/json"}
#     try:
#         response = requests.post(api_url, json=payload, headers=headers)
#         response.raise_for_status()
#         result = response.json()
#         return result.get("response", "")
#     except requests.exceptions.RequestException as e:
#         print(f"[SummarizerAgent] Error communicating with Ollama API: {e}")
#         return "[Error: Summarization failed]"
    
import requests,json

def summarize_with_ollama(input_text: str, model: str = "llama3") -> str:
    api_url = "http://ollama:11434/api/generate"
    payload = {
        "model": model,
        "prompt": input_text
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        final_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    parsed = json.loads(line.decode("utf-8"))
                    final_response += parsed.get("response", "")
                except json.JSONDecodeError:
                    continue

        return final_response.strip() if final_response else "[Error: No valid response]"

    except requests.exceptions.RequestException as e:
        print(f"[SummarizerAgent] Error communicating with Ollama API: {e}")
        return "[Error: Summarization failed]"


