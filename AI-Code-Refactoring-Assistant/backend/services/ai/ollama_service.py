import json
import os
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List

DEFAULT_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


class OllamaService:
    @staticmethod
    def _resolve_base_url(base_url: Optional[str] = None) -> str:
        if base_url and base_url.strip():
            return base_url.strip().rstrip("/")
        return DEFAULT_OLLAMA_HOST

    @staticmethod
    def is_ollama_available(base_url: Optional[str] = None) -> bool:
        url = OllamaService._resolve_base_url(base_url)
        # Try primary URL then fallback to localhost / 127.0.0.1 swap
        candidates = [url]
        if "127.0.0.1" in url:
            candidates.append(url.replace("127.0.0.1", "localhost"))
        elif "localhost" in url:
            candidates.append(url.replace("localhost", "127.0.0.1"))

        for target in candidates:
            try:
                req = urllib.request.Request(f"{target}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=2.5) as response:
                    if response.status == 200:
                        return True
            except Exception:
                continue
        return False

    @staticmethod
    def get_installed_models(base_url: Optional[str] = None) -> List[str]:
        url = OllamaService._resolve_base_url(base_url)
        candidates = [url]
        if "127.0.0.1" in url:
            candidates.append(url.replace("127.0.0.1", "localhost"))
        elif "localhost" in url:
            candidates.append(url.replace("localhost", "127.0.0.1"))

        for target in candidates:
            try:
                req = urllib.request.Request(f"{target}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        models = data.get("models", [])
                        names = [m.get("name") for m in models if m.get("name")]
                        return names
            except Exception:
                continue
        return []

    @staticmethod
    def get_best_model(preferred: Optional[str] = None, base_url: Optional[str] = None) -> str:
        installed = OllamaService.get_installed_models(base_url)
        if not installed:
            return preferred or "qwen2.5-coder"

        # Check if preferred is installed (exact match or prefix match like 'qwen2.5-coder' matching 'qwen2.5-coder:latest')
        if preferred:
            pref_lower = preferred.lower()
            for m in installed:
                if m.lower() == pref_lower or m.lower().startswith(pref_lower + ":") or pref_lower in m.lower():
                    return m

        # Look for coder models
        coder_keywords = ["coder", "code", "deepseek", "qwen", "codellama", "starcoder"]
        for kw in coder_keywords:
            for m in installed:
                if kw in m.lower():
                    return m

        # Fallback to the first installed model
        return installed[0]

    @staticmethod
    def generate(
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
        base_url: Optional[str] = None,
        system_prompt: Optional[str] = None,
        timeout: int = 90
    ) -> Optional[str]:
        target_url = OllamaService._resolve_base_url(base_url)
        if not OllamaService.is_ollama_available(target_url):
            return None

        active_model = OllamaService.get_best_model(model, target_url)

        payload: Dict[str, Any] = {
            "model": active_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{target_url}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("response", "")
        except Exception as e:
            print(f"[OllamaService] Call failed ({active_model}): {e}")
            return None

