"""
Translation service using NLLB model
"""
import logging
from typing import Dict
from app.config import NLLB_LANG_CODES, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

class TranslationService:
    """Service for translating text"""
    
    def __init__(self):
        self.initialized = False
        self.tokenizer = None
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize NLLB model"""
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            
            model_name = "facebook/nllb-200-distilled-600M"
            logger.info(f"Loading translation model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            self.initialized = True
            logger.info("Translation model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load NLLB model: {e}. Using mock translation.")
            self.initialized = False
    
    def translate(self, text: str, target_lang: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (ru, en, kk)
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {target_lang}")
        
        if not self.initialized or self.model is None:
            return self._mock_translate(text, target_lang)
        
        try:
            logger.info(f"Translating to {target_lang}: {text[:100]}...")
            
            lang_code = NLLB_LANG_CODES[target_lang]
            
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            
            with __import__('torch').no_grad():
                translated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(lang_code),
                    max_length=512
                )
            
            translated_text = self.tokenizer.batch_decode(
                translated_tokens,
                skip_special_tokens=True
            )[0]
            
            logger.info(f"Translation complete")
            return translated_text
            
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            raise
    
    def _mock_translate(self, text: str, target_lang: str) -> str:
        """Mock translation for development"""
        lang_name = SUPPORTED_LANGUAGES.get(target_lang, "Unknown")
        return f"[{lang_name}] {text}"


class MockTranslationService:
    """Mock translation service"""
    
    def translate(self, text: str, target_lang: str) -> str:
        """Return mock translation"""
        lang_map = {"ru": "RUS", "en": "ENG", "kk": "KAZ"}
        lang = lang_map.get(target_lang, "UNK")
        return f"[{lang}] {text}"
