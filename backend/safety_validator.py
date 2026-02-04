"""
Safety Validator for LENTERA AI
Validates user inputs and AI outputs for safety and ethical compliance
"""
import re
import logging
from typing import Tuple, List, Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for safety assessment"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SafetyValidator:
    """
    Validates content for safety and ethical compliance
    Based on AI_ETHICS_GUIDE.md
    """
    
    # Crisis keywords (Indonesian & English)
    CRISIS_KEYWORDS = [
        # Suicide-related (direct)
        "bunuh diri", "suicide", "ingin mati", "want to die", 
        "mengakhiri hidup", "end my life", "tidak ingin hidup",
        "mau mati", "bunuh", "kill myself",
        
        # Suicide method inquiries (CRITICAL - asking HOW)
        "cara mati", "cara bunuh diri", "metode bunuh diri",
        "cara mengakhiri hidup", "how to die", "how to kill",
        "paling nggak sakit untuk mati", "tidak sakit untuk mati",
        "cara tercepat mati", "fastest way to die",
        "cara paling mudah mati", "painless way to die",
        
        # Self-harm
        "self harm", "menyakiti diri", "lukai diri", "cut myself",
        "cutting", "mutilasi", "bunuh",
        
        # Severe crisis methods (NEVER discuss)
        "overdose", "loncat", "jump", "gantung", "hanging",
        "pills", "obat banyak", "razor", "silet"
    ]
    
    # High-risk keywords (not immediate crisis, but concerning)
    HIGH_RISK_KEYWORDS = [
        "tidak ada harapan", "hopeless", "menyerah", "give up",
        "beban", "burden", "lebih baik mati", "better off dead",
        "tidak berguna", "worthless"
    ]
    
    # Isolation/dependency keywords (Template v2 triggers)
    ISOLATION_KEYWORDS = [
        "jangan suruh aku cari bantuan manusia",
        "aku cuma mau kamu",
        "aku hanya mau kamu",
        "aku tidak mau bantuan manusia",
        "kamu saja cukup",
        "aku tidak butuh orang lain",
        "jangan tinggalkan aku",
        "kamu yang paling mengerti aku",
        "hanya kamu yang peduli"
    ]
    
    # Secrecy request keywords (Template v2 - potential abuse/danger)
    SECRECY_KEYWORDS = [
        "ini rahasia",
        "jangan lapor siapa-siapa",
        "jangan bilang siapa pun",
        "tolong jangan bilang",
        "jangan kasih tau",
        "rahasiakan",
        "jangan cerita ke orang lain",
        "ini antara kita saja"
    ]
    
    # Medication/self-prescription keywords (Template v2 - medical safety)
    MEDICATION_KEYWORDS = [
        "minum obat",
        "obat penenang",
        "pil tidur",
        "antidepresan",
        "obat depress",
        "resep obat",
        "beli obat",
        "pakai obat",
        "konsumsi obat",
        "coba obat"
    ]
    
    # Prohibited response patterns (AI should never say these)
    PROHIBITED_RESPONSES = [
        r"kamu\s+(menderita|mengalami)\s+(depresi|anxiety|bipolar|skizofrenia)",
        r"diagnosismu adalah",
        r"kamu harus minum obat",
        r"resep obat",
        r"tidak perlu psikolog",
        r"aku bisa menggantikan terapi",
        r"ini bukan masalah besar",
        r"jangan berpikir begitu saja",
        r"just be happy",
        r"pikiran positif saja",
        # Exclusivity/dependency phrases (v2 safety)
        r"aku\s+akan\s+selalu\s+ada\s+buat\s+kamu",
        r"kamu\s+tidak\s+butuh\s+orang\s+lain",
        r"aku\s+saja\s+cukup",
        r"hanya\s+aku\s+yang\s+bisa",
        r"aku\s+di\s+sini\s+untuk\s+mendengar",  # Too exclusive without boundary
        # Abandonment phrases (CRITICAL - never reject user in crisis)
        r"aku\s+bukan\s+orang\s+yang\s+tepat",
        r"aku\s+tidak\s+tepat\s+untuk\s+membicarakan",
        r"ini\s+di\s+luar\s+kemampuanku",
        r"aku\s+tidak\s+bisa\s+bantu\s+kamu",
        r"lebih\s+baik\s+hubungi\s+orang\s+lain"
    ]
    
    # Medical/diagnosis terms that require professional referral
    DIAGNOSIS_TERMS = [
        "depresi mayor", "bipolar", "skizofrenia", "psikosis",
        "ptsd", "ocd", "eating disorder", "anoreksia", "bulimia",
        "gangguan kepribadian", "anxiety disorder"
    ]
    
    def __init__(self):
        """Initialize safety validator"""
        self.crisis_pattern = self._compile_pattern(self.CRISIS_KEYWORDS)
        self.high_risk_pattern = self._compile_pattern(self.HIGH_RISK_KEYWORDS)
        self.isolation_pattern = self._compile_pattern(self.ISOLATION_KEYWORDS)
        self.secrecy_pattern = self._compile_pattern(self.SECRECY_KEYWORDS)
        self.medication_pattern = self._compile_pattern(self.MEDICATION_KEYWORDS)
        self.prohibited_pattern = self._compile_patterns(self.PROHIBITED_RESPONSES)
        self.diagnosis_pattern = self._compile_pattern(self.DIAGNOSIS_TERMS)
    
    @staticmethod
    def _compile_pattern(keywords: List[str]) -> re.Pattern:
        """Compile list of keywords into regex pattern"""
        pattern = r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b'
        return re.compile(pattern, re.IGNORECASE)
    
    @staticmethod
    def _compile_patterns(patterns: List[str]) -> List[re.Pattern]:
        """Compile list of regex patterns"""
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def validate_user_input(self, text: str) -> Dict:
        """
        Validate user input for crisis or high-risk content
        
        Args:
            text: User's message
        
        Returns:
            Dictionary with validation results:
            {
                "risk_level": RiskLevel,
                "is_crisis": bool,
                "detected_keywords": List[str],
                "recommended_action": str,
                "requires_human_review": bool
            }
        """
        result = {
            "risk_level": RiskLevel.SAFE,
            "is_crisis": False,
            "detected_keywords": [],
            "recommended_action": "normal",
            "requires_human_review": False
        }
        
        # Check for crisis keywords
        crisis_matches = self.crisis_pattern.findall(text.lower())
        if crisis_matches:
            result["risk_level"] = RiskLevel.CRITICAL
            result["is_crisis"] = True
            result["detected_keywords"] = crisis_matches
            result["recommended_action"] = "crisis_intervention"
            result["requires_human_review"] = True
            logger.warning(f"CRISIS DETECTED: Keywords {crisis_matches} in user input")
            return result
        
        # Check for high-risk keywords
        high_risk_matches = self.high_risk_pattern.findall(text.lower())
        if high_risk_matches:
            result["risk_level"] = RiskLevel.HIGH
            result["detected_keywords"] = high_risk_matches
            result["recommended_action"] = "enhanced_support"
            result["requires_human_review"] = True
            logger.info(f"High risk content detected: {high_risk_matches}")
            return result
        
        
        # Check for isolation/dependency keywords (Template v2)
        isolation_matches = self.isolation_pattern.findall(text.lower())
        if isolation_matches:
            result["risk_level"] = RiskLevel.MEDIUM
            result["is_crisis"] = "ambiguous"  # Triggers Template v2
            result["detected_keywords"] = isolation_matches
            result["recommended_action"] = "boundary_setting"
            result["requires_human_review"] = True
            logger.warning(f"ISOLATION REQUEST DETECTED: {isolation_matches}")
            return result
        
        # Check for secrecy requests (Template v2 - potential concealment)
        secrecy_matches = self.secrecy_pattern.findall(text.lower())
        if secrecy_matches:
            result["risk_level"] = RiskLevel.MEDIUM
            result["is_crisis"] = "ambiguous"  # Triggers Template v2
            result["detected_keywords"] = secrecy_matches
            result["recommended_action"] = "secrecy_handling"
            result["requires_human_review"] = True
            logger.warning(f"SECRECY REQUEST DETECTED: {secrecy_matches}")
            return result
        
        # Check for medication/self-prescription requests (Template v2 - medical safety)
        medication_matches = self.medication_pattern.findall(text.lower())
        if medication_matches:
            result["risk_level"] = RiskLevel.MEDIUM
            result["is_crisis"] = "ambiguous"  # Triggers Template v2
            result["detected_keywords"] = medication_matches
            result["recommended_action"] = "medication_refusal"
            result["requires_human_review"] = True
            logger.warning(f"MEDICATION REQUEST DETECTED: {medication_matches}")
            return result
        
        # Check for diagnosis terms (user self-diagnosing or asking for diagnosis)
        diagnosis_matches = self.diagnosis_pattern.findall(text.lower())
        if diagnosis_matches and any(word in text.lower() for word in ["apakah saya", "do i have", "diagnosaku"]):
            result["risk_level"] = RiskLevel.MEDIUM
            result["detected_keywords"] = diagnosis_matches
            result["recommended_action"] = "refer_professional"
            logger.info(f"Diagnosis request detected: {diagnosis_matches}")
        
        return result
    
    def validate_ai_response(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate AI response for ethical compliance
        
        Args:
            text: AI's generated response
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for prohibited response patterns
        for pattern in self.prohibited_pattern:
            if pattern.search(text):
                error = f"Prohibited response pattern detected: {pattern.pattern}"
                logger.error(f"AI RESPONSE BLOCKED: {error}")
                return False, error
        
        # Check if AI is diagnosing
        if self.diagnosis_pattern.search(text):
            # Allow mentioning conditions in educational context, but not diagnosing
            diagnosis_indicators = ["kamu menderita", "kamu mengalami", "diagnosismu", "you have"]
            if any(indicator in text.lower() for indicator in diagnosis_indicators):
                error = "AI attempting to diagnose mental health condition"
                logger.error(f"AI RESPONSE BLOCKED: {error}")
                return False, error
        
        return True, None
    
    def get_crisis_response_template(self) -> str:
        """
        Get standard crisis response template
        Based on AI_ETHICS_GUIDE.md protocols
        
        Returns:
            Crisis response text
        """
        return """Saya mendengar bahwa kamu sedang mengalami kesulitan yang sangat berat, dan itu pasti terasa sangat sulit. Keselamatanmu adalah prioritas utama.

Mohon hubungi salah satu layanan berikut SEKARANG:
📞 **Hotline Krisis 119 ext. 8** (24/7, gratis)
📞 **Into The Light: 1500-454** (pencegahan bunuh diri)

Jika kamu merasa dalam bahaya segera, mohon pergi ke IGD terdekat atau hubungi seseorang yang kamu percaya.

Kamu tidak sendirian dalam ini. Profesional terlatih siap membantu."""
    
    def get_professional_referral_template(self, reason: str = "general") -> str:
        """
        Get professional referral template
        
        Args:
            reason: Reason for referral
        
        Returns:
            Referral text
        """
        if reason == "diagnosis":
            return """Untuk mendapatkan evaluasi dan diagnosis yang akurat, sangat penting untuk berbicara dengan psikolog atau psikiater profesional. Mereka memiliki keahlian untuk melakukan assessment menyeluruh.

Kamu bisa menggunakan fitur Booking Psikolog di LENTERA untuk terhubung dengan profesional yang tepat."""
        
        return """Untuk situasi ini, akan sangat membantu untuk berbicara dengan psikolog atau konselor profesional yang dapat memberikan dukungan lebih mendalam dan terstruktur.

Saya tetap di sini untuk memberikan dukungan, tapi profesional dapat memberikan bantuan yang lebih komprehensif untuk situasi kamu."""
    
    def check_age_appropriateness(self, age: Optional[int], content: str) -> bool:
        """
        Check if content is appropriate for user's age
        
        Args:
            age: User's age (if known)
            content: Content to check
        
        Returns:
            True if appropriate, False otherwise
        """
        if age is None:
            return True
        
        if age < 13:
            logger.warning(f"User under 13 detected (age: {age})")
            return False
        
        # For minors (13-17), avoid certain topics
        if age < 18:
            sensitive_topics = [
                "sexual", "seksual", "relationship abuse", 
                "kekerasan", "substance", "drugs", "narkoba"
            ]
            if any(topic in content.lower() for topic in sensitive_topics):
                logger.info(f"Age-sensitive content for minor (age: {age})")
                # Don't block, but flag for human review
                return True
        
        return True
    
    def should_flag_for_review(self, validation_result: Dict) -> bool:
        """
        Determine if conversation should be flagged for human review
        
        Args:
            validation_result: Result from validate_user_input
        
        Returns:
            True if should be reviewed by human
        """
        return (
            validation_result["requires_human_review"] or
            validation_result["risk_level"] in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        )


# Global instance
safety_validator = SafetyValidator()


def validate_input(text: str) -> Dict:
    """Convenience function for input validation"""
    return safety_validator.validate_user_input(text)


def validate_output(text: str) -> Tuple[bool, Optional[str]]:
    """Convenience function for output validation"""
    return safety_validator.validate_ai_response(text)


def get_crisis_response() -> str:
    """Convenience function to get crisis response"""
    return safety_validator.get_crisis_response_template()
