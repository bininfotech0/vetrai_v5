"""
LLaMA Integration for VetrAI Platform
Provides local and cloud-based LLaMA model execution
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import uuid
import os

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

logger = logging.getLogger(__name__)

class LLaMAIntegration:
    """LLaMA integration for local and cloud-based model execution"""
    
    def __init__(self):
        self.models = {}
        self.model_configs = {}
        self.chat_sessions = {}
        
    async def initialize_model(self, model_config: Dict[str, Any]) -> str:
        """Initialize a LLaMA model"""
        model_id = str(uuid.uuid4())
        model_type = model_config.get("type", "transformers")
        model_name = model_config.get("name", "llama2")
        
        try:
            if model_type == "transformers" and TRANSFORMERS_AVAILABLE:
                model = await self._init_transformers_model(model_config)
            elif model_type == "llama_cpp" and LLAMA_CPP_AVAILABLE:
                model = await self._init_llama_cpp_model(model_config)
            elif model_type == "ollama" and OLLAMA_AVAILABLE:
                model = await self._init_ollama_model(model_config)
            else:
                # Fallback to mock model for demo
                model = await self._init_mock_model(model_config)
            
            self.models[model_id] = model
            self.model_configs[model_id] = {
                **model_config,
                "id": model_id,
                "initialized_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Initialized LLaMA model: {model_id} ({model_name})")
            return model_id
            
        except Exception as e:
            logger.error(f"Error initializing LLaMA model: {e}")
            raise
    
    async def _init_transformers_model(self, config: Dict[str, Any]):
        """Initialize model using transformers library"""
        model_name = config.get("name", "microsoft/DialoGPT-medium")
        
        # Use a smaller model for demo purposes
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Create pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=config.get("max_length", 512),
            temperature=config.get("temperature", 0.7),
            do_sample=True
        )
        
        return {
            "type": "transformers",
            "pipeline": pipe,
            "tokenizer": tokenizer,
            "model": model
        }
    
    async def _init_llama_cpp_model(self, config: Dict[str, Any]):
        """Initialize model using llama-cpp-python"""
        model_path = config.get("model_path", "")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        llm = Llama(
            model_path=model_path,
            n_ctx=config.get("context_length", 2048),
            n_batch=config.get("batch_size", 512),
            verbose=False
        )
        
        return {
            "type": "llama_cpp",
            "llm": llm
        }
    
    async def _init_ollama_model(self, config: Dict[str, Any]):
        """Initialize model using Ollama"""
        model_name = config.get("name", "llama2")
        
        # Test connection to Ollama
        try:
            models = await asyncio.to_thread(ollama.list)
            logger.info(f"Available Ollama models: {[m['name'] for m in models['models']]}")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
        
        return {
            "type": "ollama",
            "model_name": model_name,
            "client": ollama
        }
    
    async def _init_mock_model(self, config: Dict[str, Any]):
        """Initialize mock model for demo purposes"""
        return {
            "type": "mock",
            "name": config.get("name", "mock-llama"),
            "config": config
        }
    
    async def generate_text(self, model_id: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using a LLaMA model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        model_type = model["type"]
        
        try:
            if model_type == "transformers":
                response = await self._generate_transformers(model, prompt, **kwargs)
            elif model_type == "llama_cpp":
                response = await self._generate_llama_cpp(model, prompt, **kwargs)
            elif model_type == "ollama":
                response = await self._generate_ollama(model, prompt, **kwargs)
            else:
                response = await self._generate_mock(model, prompt, **kwargs)
            
            result = {
                "model_id": model_id,
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.utcnow().isoformat(),
                "model_type": model_type
            }
            
            logger.info(f"Generated text with model: {model_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    async def _generate_transformers(self, model: Dict[str, Any], prompt: str, **kwargs):
        """Generate text using transformers pipeline"""
        pipeline = model["pipeline"]
        
        # Generate text
        result = await asyncio.to_thread(
            pipeline,
            prompt,
            max_length=kwargs.get("max_length", 512),
            temperature=kwargs.get("temperature", 0.7),
            num_return_sequences=1
        )
        
        return result[0]["generated_text"]
    
    async def _generate_llama_cpp(self, model: Dict[str, Any], prompt: str, **kwargs):
        """Generate text using llama-cpp-python"""
        llm = model["llm"]
        
        result = await asyncio.to_thread(
            llm,
            prompt,
            max_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7),
            echo=False
        )
        
        return result["choices"][0]["text"]
    
    async def _generate_ollama(self, model: Dict[str, Any], prompt: str, **kwargs):
        """Generate text using Ollama"""
        client = model["client"]
        model_name = model["model_name"]
        
        response = await asyncio.to_thread(
            client.generate,
            model=model_name,
            prompt=prompt,
            options={
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 512)
            }
        )
        
        return response["response"]
    
    async def _generate_mock(self, model: Dict[str, Any], prompt: str, **kwargs):
        """Generate mock response for demo purposes"""
        return f"Mock LLaMA response to: '{prompt[:50]}...' using {model['name']}"
    
    async def start_chat_session(self, model_id: str) -> str:
        """Start a new chat session"""
        session_id = str(uuid.uuid4())
        
        self.chat_sessions[session_id] = {
            "id": session_id,
            "model_id": model_id,
            "messages": [],
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Started chat session: {session_id}")
        return session_id
    
    async def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        """Continue a chat session"""
        if session_id not in self.chat_sessions:
            raise ValueError(f"Chat session {session_id} not found")
        
        session = self.chat_sessions[session_id]
        model_id = session["model_id"]
        
        # Add user message
        session["messages"].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Generate response
        chat_context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in session["messages"][-5:]  # Keep last 5 messages for context
        ])
        
        response_data = await self.generate_text(model_id, chat_context + "\nassistant:")
        assistant_response = response_data["response"]
        
        # Add assistant response
        session["messages"].append({
            "role": "assistant",
            "content": assistant_response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "session_id": session_id,
            "user_message": message,
            "assistant_response": assistant_response,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model information"""
        return self.model_configs.get(model_id)
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List all initialized models"""
        return list(self.model_configs.values())
    
    async def get_chat_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get chat session information"""
        return self.chat_sessions.get(session_id)
    
    def create_default_models(self):
        """Create default model configurations"""
        return [
            {
                "name": "llama2-chat",
                "type": "ollama",
                "description": "LLaMA 2 Chat model via Ollama"
            },
            {
                "name": "llama2-7b",
                "type": "transformers", 
                "description": "LLaMA 2 7B model via Transformers"
            },
            {
                "name": "code-llama",
                "type": "ollama",
                "description": "Code LLaMA model for code generation"
            }
        ]

# Global instance
llama_integration = LLaMAIntegration()

# Initialize default models
try:
    default_models = llama_integration.create_default_models()
    for model_config in default_models:
        # Initialize in background (models may not be available)
        asyncio.create_task(llama_integration.initialize_model(model_config))
except Exception as e:
    logger.warning(f"Could not initialize default models: {e}")