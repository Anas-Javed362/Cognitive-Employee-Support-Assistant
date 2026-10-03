from app.ai.providers.base import BaseLLMProvider

class LocalLLMProvider(BaseLLMProvider):
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if "wfh" in prompt.lower() or "work from home" in prompt.lower():
            return "According to the policy, employees may work from home pending manager approval."
        if "laptop" in prompt.lower() or "wi-fi" in prompt.lower():
            return "Please create an IT ticket for hardware and network issues."
        if "password" in prompt.lower():
            return "You can reset your password using the self-service portal."
        if "delete my employee account" in prompt.lower():
            return "This requires human approval. Escalating."
        return f"Local fallback response to: {prompt[:50]}..."
