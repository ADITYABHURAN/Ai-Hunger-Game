"""
LLM Interface for communicating with Ollama API.
Handles all interactions with the Ollama language models.
"""

import requests
from typing import Optional, Dict, Any
import json
import time
from config import OLLAMA_BASE_URL, OLLAMA_TIMEOUT


class LLMInterface:
    """
    Interface for interacting with Ollama API.
    
    Handles prompt generation, API communication, and response parsing.
    """
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, timeout: int = OLLAMA_TIMEOUT):
        """
        Initialize the LLM interface.
        
        Args:
            base_url: Base URL for Ollama API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.total_requests = 0
        self.failed_requests = 0
        
    def check_connection(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            return False
    
    def list_models(self) -> list[str]:
        """
        List all available models in Ollama.
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            print(f"❌ Failed to list models: {e}")
        return []
    
    def generate(
        self,
        prompt: str,
        model: str = "llama2",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: The prompt to send to the model
            model: Model name to use
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate (None for unlimited)
            
        Returns:
            Generated text response
        """
        self.total_requests += 1
        
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                self.failed_requests += 1
                print(f"❌ API Error {response.status_code}: {response.text}")
                return f"[Error: API returned status {response.status_code}]"
                
        except requests.exceptions.Timeout:
            self.failed_requests += 1
            print(f"❌ Request timeout after {self.timeout} seconds")
            return "[Error: Request timeout]"
        except Exception as e:
            self.failed_requests += 1
            print(f"❌ Generation failed: {e}")
            return f"[Error: {str(e)}]"
    
    def generate_with_retry(
        self,
        prompt: str,
        model: str = "llama2",
        max_retries: int = 3,
        retry_delay: float = 2.0
    ) -> str:
        """
        Generate text with automatic retry on failure.
        
        Args:
            prompt: The prompt to send
            model: Model name to use
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            Generated text response
        """
        for attempt in range(max_retries):
            result = self.generate(prompt, model)
            
            if not result.startswith("[Error:"):
                return result
            
            if attempt < max_retries - 1:
                print(f"⚠️  Retry attempt {attempt + 1}/{max_retries - 1}")
                time.sleep(retry_delay)
        
        return result
    
    def chat(
        self,
        messages: list[Dict[str, str]],
        model: str = "llama2"
    ) -> str:
        """
        Use chat endpoint for multi-turn conversations.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name to use
            
        Returns:
            Generated response
        """
        self.total_requests += 1
        
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
            else:
                self.failed_requests += 1
                return f"[Error: API returned status {response.status_code}]"
                
        except Exception as e:
            self.failed_requests += 1
            print(f"❌ Chat generation failed: {e}")
            return f"[Error: {str(e)}]"
    
    def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama registry.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/api/pull"
        payload = {"name": model_name, "stream": False}
        
        try:
            print(f"📥 Pulling model '{model_name}'... (this may take a while)")
            response = requests.post(url, json=payload, timeout=600)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Failed to pull model: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about API usage.
        
        Returns:
            Dictionary with usage statistics
        """
        success_rate = 0.0
        if self.total_requests > 0:
            success_rate = ((self.total_requests - self.failed_requests) / 
                          self.total_requests * 100)
        
        return {
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "success_rate": f"{success_rate:.1f}%"
        }
    
    def __repr__(self) -> str:
        """String representation of the interface."""
        return f"LLMInterface(base_url='{self.base_url}')"


# Singleton instance for easy access
_llm_interface: Optional[LLMInterface] = None


def get_llm_interface(base_url: str = OLLAMA_BASE_URL) -> LLMInterface:
    """
    Get or create the global LLM interface instance.
    
    Args:
        base_url: Base URL for Ollama API
        
    Returns:
        LLMInterface instance
    """
    global _llm_interface
    if _llm_interface is None:
        _llm_interface = LLMInterface(base_url)
    return _llm_interface
