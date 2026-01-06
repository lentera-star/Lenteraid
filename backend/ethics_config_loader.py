"""
Ethics Configuration Loader for LENTERA
Loads and validates ethics rules from YAML configuration
"""
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class EthicsConfig:
    """Load and manage ethics configuration from YAML"""
    
    def __init__(self, config_path: str = "ethics_config.yaml"):
        """
        Initialize ethics configuration
        
        Args:
            config_path: Path to YAML config file
        """
        self.config_path = Path(config_path)
        self.config: Dict = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Ethics config loaded from {self.config_path}")
            self._validate_config()
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise
    
    def _validate_config(self):
        """Validate required configuration sections"""
        required_sections = [
            'principles', 'crisis', 'prohibited', 
            'disclaimers', 'cultural', 'data_protection'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")
        
        logger.info("Ethics config validation passed")
    
    # ========== Crisis Configuration ==========
    
    def get_crisis_keywords(self, level: str = "critical") -> List[str]:
        """
        Get crisis keywords by severity level
        
        Args:
            level: "critical" or "high_risk"
        
        Returns:
            List of keywords
        """
        return self.config['crisis']['detection']['keywords'].get(level, [])
    
    def get_all_crisis_keywords(self) -> List[str]:
        """Get all crisis keywords (critical + high_risk)"""
        critical = self.get_crisis_keywords('critical')
        high_risk = self.get_crisis_keywords('high_risk')
        return critical + high_risk
    
    def get_hotline(self, hotline_type: str = "primary") -> Dict:
        """
        Get hotline information
        
        Args:
            hotline_type: "primary", "suicide_prevention", "child_protection", "women_crisis"
        
        Returns:
            Dictionary with hotline info
        """
        return self.config['crisis']['response']['hotlines'].get(hotline_type, {})
    
    def get_all_hotlines(self) -> Dict:
        """Get all configured hotlines"""
        return self.config['crisis']['response']['hotlines']
    
    def get_crisis_response_template(self) -> str:
        """Get crisis response template text"""
        return self.config['crisis']['response']['template']
    
    # ========== Prohibited Patterns ==========
    
    def get_prohibited_patterns(self, category: str = None) -> List[str]:
        """
        Get prohibited response patterns
        
        Args:
            category: "diagnosis", "medication", "replacement", "toxic_positivity", or None for all
        
        Returns:
            List of prohibited patterns
        """
        if category:
            return self.config['prohibited'].get(category, {}).get('patterns', [])
        
        # Return all patterns
        all_patterns = []
        for cat in self.config['prohibited'].values():
            if isinstance(cat, dict) and 'patterns' in cat:
                all_patterns.extend(cat['patterns'])
        return all_patterns
    
    def get_prohibited_conditions(self) -> List[str]:
        """Get list of mental health conditions AI cannot diagnose"""
        return self.config['prohibited']['diagnosis'].get('conditions', [])
    
    # ========== Disclaimers ==========
    
    def get_disclaimer(self, disclaimer_type: str = "conversation_start") -> str:
        """
        Get disclaimer text
        
        Args:
            disclaimer_type: "conversation_start", "professional_referral"
        
        Returns:
            Disclaimer text
        """
        return self.config['disclaimers'].get(disclaimer_type, {}).get('text', '')
    
    def get_user_agreement_points(self) -> List[str]:
        """Get user agreement bullet points"""
        return self.config['disclaimers']['user_agreement'].get('points', [])
    
    # ========== Cultural Settings ==========
    
    def get_cultural_settings(self) -> Dict:
        """Get all cultural sensitivity settings"""
        return self.config.get('cultural', {})
    
    def get_derogatory_terms(self) -> List[str]:
        """Get list of derogatory terms to avoid"""
        return self.config['cultural']['stigma'].get('avoid_derogatory_terms', [])
    
    def get_language_style(self) -> str:
        """Get language style (formal/informal)"""
        return self.config['cultural']['language'].get('style', 'informal')
    
    # ========== Age Settings ==========
    
    def get_minimum_age(self) -> int:
        """Get minimum required age"""
        return self.config['age'].get('minimum_age', 13)
    
    def is_age_appropriate(self, age: Optional[int]) -> bool:
        """Check if user age is appropriate"""
        if age is None:
            return True
        return age >= self.get_minimum_age()
    
    def get_age_restrictions(self, age: int) -> Dict:
        """Get age-specific restrictions and requirements"""
        if age < 13:
            return {"access": "prohibited"}
        elif age < 18:
            return self.config['age'].get('under_18', {})
        return {}
    
    # ========== Personality Settings ==========
    
    def get_personality_traits(self) -> Dict:
        """Get AI personality configuration"""
        return self.config.get('personality', {})
    
    def get_response_structure(self) -> Dict:
        """Get recommended response structure"""
        return self.config['personality'].get('response_structure', {})
    
    def get_max_response_length(self) -> Dict:
        """Get response length limits"""
        return self.config['personality'].get('max_response_length', {})
    
    # ========== Professional Referral ==========
    
    def get_referral_criteria(self) -> List[str]:
        """Get list of situations requiring professional referral"""
        return self.config['referral'].get('when_to_refer', [])
    
    def get_professional_resources(self) -> Dict:
        """Get professional organization resources"""
        return self.config['referral'].get('resources', {})
    
    # ========== Data Protection ==========
    
    def is_uu_pdp_compliant(self) -> bool:
        """Check if UU PDP compliance is enabled"""
        return self.config['data_protection'].get('uu_pdp_compliance', False)
    
    def get_data_protection_principles(self) -> Dict:
        """Get data protection principles"""
        return self.config['data_protection'].get('principles', {})
    
    def get_user_data_rights(self) -> Dict:
        """Get user rights regarding their data"""
        return self.config['data_protection'].get('user_rights', {})
    
    # ========== Quality Assurance ==========
    
    def get_qa_checklist(self) -> List[str]:
        """Get pre-response quality checklist"""
        return self.config['quality_assurance'].get('pre_response_checklist', [])
    
    def get_human_review_triggers(self) -> List[str]:
        """Get triggers for human review"""
        return self.config['quality_assurance'].get('human_review_triggers', [])
    
    # ========== Operational Parameters ==========
    
    def get_rate_limits(self) -> Dict:
        """Get rate limiting configuration"""
        return self.config['operations'].get('rate_limiting', {})
    
    def get_response_time_target(self) -> int:
        """Get target response time in seconds"""
        return self.config['operations'].get('response_time_target_seconds', 5)
    
    # ========== Utility Methods ==========
    
    def get_version(self) -> str:
        """Get configuration version"""
        return self.config['implementation'].get('version', 'unknown')
    
    def get_last_updated(self) -> str:
        """Get last update date"""
        return self.config['implementation'].get('last_updated', 'unknown')
    
    def get_implementation_status(self) -> Dict:
        """Get implementation checklist status"""
        return self.config['implementation'].get('checklist', {})
    
    def __repr__(self) -> str:
        return f"EthicsConfig(version={self.get_version()}, last_updated={self.get_last_updated()})"


# Global instance
ethics_config: Optional[EthicsConfig] = None


def load_ethics_config(config_path: str = "ethics_config.yaml") -> EthicsConfig:
    """
    Load ethics configuration (singleton pattern)
    
    Args:
        config_path: Path to YAML config
    
    Returns:
        EthicsConfig instance
    """
    global ethics_config
    
    if ethics_config is None:
        ethics_config = EthicsConfig(config_path)
    
    return ethics_config


def get_ethics_config() -> EthicsConfig:
    """Get current ethics configuration instance"""
    if ethics_config is None:
        return load_ethics_config()
    return ethics_config
