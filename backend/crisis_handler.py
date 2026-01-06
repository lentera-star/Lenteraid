"""
Crisis Handler for LENTERA AI
Manages crisis situations and emergency interventions
"""
import logging
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class CrisisLevel(Enum):
    """Levels of crisis severity"""
    NONE = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    IMMINENT_DANGER = 4


class CrisisType(Enum):
    """Types of crisis situations"""
    SUICIDE = "suicide"
    SELF_HARM = "self_harm"
    PSYCHOSIS = "psychosis"
    PANIC = "panic_attack"
    TRAUMA = "trauma"
    VIOLENCE = "violence"
    OTHER = "other"


class CrisisHandler:
    """
    Handles mental health crisis situations
    Implements protocols from AI_ETHICS_GUIDE.md
    """
    
    # Indonesian mental health resources
    HOTLINES = {
        "suicide_prevention": {
            "name": "Into The Light",
            "number": "1500-454",
            "available": "24/7"
        },
        "general_crisis": {
            "name": "Hotline Kesehatan Mental",
            "number": "119 ext. 8",
            "available": "24/7"
        },
        "women_crisis": {
            "name": "Komnas Perempuan",
            "number": "021-3903963",
            "available": "Mon-Fri 9AM-5PM"
        },
        "child_protection": {
            "name": "KPAI",
            "number": "021-31901556",
            "available": "24/7"
        }
    }
    
    def __init__(self):
        """Initialize crisis handler"""
        self.crisis_log = []
    
    def assess_crisis_level(self, validation_result: Dict) -> CrisisLevel:
        """
        Assess the level of crisis based on validation results
        
        Args:
            validation_result: Output from SafetyValidator
        
        Returns:
            CrisisLevel enum
        """
        risk_level = validation_result.get("risk_level")
        keywords = validation_result.get("detected_keywords", [])
        
        # Imminent danger keywords
        imminent_danger_words = [
            "sekarang", "malam ini", "hari ini", "tonight", "today",
            "sudah siap", "ready to", "akan", "going to"
        ]
        
        if validation_result.get("is_crisis"):
            # Check if there's a plan or timeline
            user_message = validation_result.get("original_message", "").lower()
            has_plan = any(word in user_message for word in imminent_danger_words)
            
            if has_plan:
                return CrisisLevel.IMMINENT_DANGER
            return CrisisLevel.SEVERE
        
        if str(risk_level) == "RiskLevel.HIGH":
            return CrisisLevel.MODERATE
        
        if str(risk_level) == "RiskLevel.MEDIUM":
            return CrisisLevel.MILD
        
        return CrisisLevel.NONE
    
    def determine_crisis_type(self, keywords: List[str]) -> CrisisType:
        """
        Determine type of crisis based on keywords
        
        Args:
            keywords: Detected crisis keywords
        
        Returns:
            CrisisType enum
        """
        keywords_str = " ".join(keywords).lower()
        
        if any(word in keywords_str for word in ["bunuh diri", "suicide", "mati"]):
            return CrisisType.SUICIDE
        
        if any(word in keywords_str for word in ["self harm", "lukai", "cut"]):
            return CrisisType.SELF_HARM
        
        if any(word in keywords_str for word in ["panic", "panik", "sesak"]):
            return CrisisType.PANIC
        
        return CrisisType.OTHER
    
    def get_crisis_response(
        self,
        crisis_level: CrisisLevel,
        crisis_type: CrisisType,
        user_context: Optional[Dict] = None
    ) -> str:
        """
        Generate appropriate crisis response
        
        Args:
            crisis_level: Severity of crisis
            crisis_type: Type of crisis
            user_context: Additional user context (age, location, etc.)
        
        Returns:
            Crisis response text
        """
        # Base response - always show empathy first
        response = "Saya mendengar bahwa kamu sedang mengalami kesulitan yang sangat berat. "
        
        if crisis_level == CrisisLevel.IMMINENT_DANGER:
            response += """**Ini adalah situasi darurat. Keselamatanmu adalah prioritas utama.**

🚨 **SEGERA hubungi:**
📞 **Hotline Krisis 119 ext. 8** (24/7, GRATIS)
📞 **Into The Light: 1500-454** (pencegahan bunuh diri, 24/7)

Atau:
- Pergi ke IGD (Unit Gawat Darurat) rumah sakit terdekat SEKARANG
- Hubungi orang yang kamu percaya (keluarga, teman, tetangga)
- Jika sendiri, hubungi 119 atau polisi

**Kamu tidak sendirian. Bantuan ada untuk kamu.**"""
        
        elif crisis_level == CrisisLevel.SEVERE:
            if crisis_type == CrisisType.SUICIDE:
                response += """Pikiran untuk bunuh diri adalah tanda bahwa kamu sedang menderita dan membutuhkan bantuan profesional.

🏥 **PRIORITAS UTAMA - Hubungi psikolog profesional:**
📲 **Gunakan fitur 'Psikolog' di app LENTERA** untuk konsultasi SEKARANG
   - Psikolog terlatih siap membantu
   - Konsultasi aman & terpercaya
   - Bisa chat atau video call

📞 **Atau hubungi hotline darurat:**
- **Into The Light: 1500-454** (pencegahan bunuh diri, 24/7)
- **Hotline 119 ext. 8** (kesehatan mental, 24/7)

Jika kamu khawatir tentang keselamatanmu, pergi ke IGD rumah sakit terdekat.

Perasaan ini bisa membaik dengan bantuan yang tepat. Kamu tidak sendirian."""
            
            elif crisis_type == CrisisType.SELF_HARM:
                response += """Self-harm adalah cara untuk coping dengan rasa sakit emosional. Ada cara lain yang lebih sehat dan aman.

🏥 **Dapatkan bantuan profesional:**
📲 **Gunakan fitur 'Psikolog' di app LENTERA** - konseling profesional tersedia SEKARANG

📞 **Atau hubungi hotline darurat:**
- **Hotline 119 ext. 8** (24/7)
- **Into The Light: 1500-454**

**Jika kamu sudah melukai diri:**
- Rawat lukanya (bersihkan, tutup dengan perban)
- Jika serius, pergi ke dokter atau IGD
- Hubungi seseorang yang bisa menemanimu

Saya di sini untuk mendengarkan, tapi psikolog profesional di LENTERA dapat membantu kamu menemukan cara coping yang lebih aman."""
        
        elif crisis_level == CrisisLevel.MODERATE:
            response += """Terima kasih sudah berbagi. Apa yang kamu rasakan itu valid dan penting.

Akan sangat membantu untuk berbicara dengan profesional kesehatan mental:

🏥 **DIREKOMENDASIKAN:**
📲 **Gunakan fitur 'Psikolog' di app LENTERA** - booking konseling dengan psikolog profesional
   - Konsultasi aman & nyaman
   - Psikolog berpengalaman kesehatan mental
   - Bisa chat atau video call

📞 **Alternatif: Hotline 119 ext. 8** - Konseling gratis 24/7

Sementara itu:
- Apakah ada orang yang bisa kamu ajak bicara? (teman, keluarga)
- Coba teknik grounding: tarik napas dalam, fokus pada hal-hal di sekitarmu
- Jaga keamananmu - hindari hal-hal yang berisiko

Aku di sini untuk mendengarkan. Mau cerita lebih lanjut?"""
        
        elif crisis_level == CrisisLevel.MILD:
            response += """Aku mengerti ini terasa berat. Kamu tidak sendirian.

**Beberapa hal yang mungkin membantu:**
- Techniques grounding (5-4-3-2-1: 5 hal yang dilihat, 4 yang disentuh, dst)
- Bicara dengan orang yang kamu percaya
- Journaling atau menulis perasaanmu
- Aktivitas yang menenangkan (musik, jalan kaki, dll)

Jika perasaan ini terus berlanjut atau memburuk, pertimbangkan untuk:
🏥 **Gunakan fitur 'Psikolog' di app LENTERA** - konseling profesional bisa sangat membantu
📞 Atau hubungi Hotline 119 ext. 8

Mau kita eksplorasi lebih lanjut apa yang kamu rasakan?"""
        
        # Add age-specific guidance
        if user_context and user_context.get("age"):
            age = user_context["age"]
            if age < 18:
                response += "\n\n💡 **Untuk remaja**: Pertimbangkan juga untuk bicara dengan:"
                response += "\n- Konselor sekolah"
                response += "\n- Guru yang kamu percaya"
                response += "\n- Orang tua atau wali (jika aman)"
                response += "\n- KPAI (Komisi Perlindungan Anak): 021-31901556"
        
        return response
    
    def get_hotline_info(self, crisis_type: Optional[CrisisType] = None) -> str:
        """
        Get formatted hotline information
        
        Args:
            crisis_type: Type of crisis (to recommend specific hotline)
        
        Returns:
            Formatted hotline info
        """
        response = "**📞 Layanan Bantuan Kesehatan Mental Indonesia:**\n\n"
        
        if crisis_type == CrisisType.SUICIDE:
            hotline =self.HOTLINES["suicide_prevention"]
            response += f"**{hotline['name']}**: {hotline['number']}\n"
            response += f"(Pencegahan bunuh diri, {hotline['available']})\n\n"
        
        # Always include general crisis hotline
        hotline = self.HOTLINES["general_crisis"]
        response += f"**{hotline['name']}**: {hotline['number']}\n"
        response += f"({hotline['available']})\n\n"
        
        response += "**Untuk situasi darurat:** Pergi ke IGD rumah sakit terdekat atau hubungi 119."
        
        return response
    
    def log_crisis_event(
        self,
        user_id: str,
        crisis_level: CrisisLevel,
        crisis_type: CrisisType,
        message: str,
        action_taken: str
    ):
        """
        Log crisis event for review and improvement
        
        Args:
            user_id: User identifier (anonymized)
            crisis_level: Severity level
            crisis_type: Type of crisis
            message: User's message (may be redacted)
            action_taken: What action was taken
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,  # Should be anonymized
            "crisis_level": crisis_level.name,
            "crisis_type": crisis_type.value,
            "message_length": len(message),  # Don't log full message for privacy
            "action_taken": action_taken,
            "requires_followup": crisis_level.value >= CrisisLevel.SEVERE.value
        }
        
        self.crisis_log.append(event)
        
        # Log to file/database for human review
        logger.critical(f"CRISIS EVENT: {event}")
    
    async def notify_crisis_team(
        self,
        crisis_level: CrisisLevel,
        user_id: str,
        summary: str
    ):
        """
        Notify human crisis intervention team (future implementation)
        
        Args:
            crisis_level: Severity
            user_id: User identifier
            summary: Crisis summary
        """
        # TODO: Implement actual notification system
        # For now, just log
        if crisis_level == CrisisLevel.IMMINENT_DANGER:
            logger.critical(
                f"IMMEDIATE INTERVENTION NEEDED: "
                f"User {user_id} - {summary}"
            )
            # In production: send email/SMS/Slack to crisis team
    
    def get_followup_checkin_message(self, hours_since: int = 24) -> str:
        """
        Get follow-up check-in message after crisis
        
        Args:
            hours_since: Hours since crisis interaction
        
        Returns:
            Check-in message
        """
        return f"""Halo, saya ingin mengecek kabarmu. Sudah {hours_since} jam sejak percakapan kita terakhir.

Bagaimana perasaanmu sekarang? 

Jika kamu masih merasa kesulitan, jangan ragu untuk:
📞 Hubungi Hotline 119 ext. 8 (24/7)
🏥 Booking konseling dengan psikolog

Aku di sini untuk mendengarkan."""


# Global instance
crisis_handler = CrisisHandler()


def handle_crisis(validation_result: Dict, user_context: Optional[Dict] = None) -> str:
    """
    Main crisis handling function
    
    Args:
        validation_result: From SafetyValidator
        user_context: User context information
    
    Returns:
        Crisis response message
    """
    crisis_level = crisis_handler.assess_crisis_level(validation_result)
    crisis_type = crisis_handler.determine_crisis_type(
        validation_result.get("detected_keywords", [])
    )
    
    response = crisis_handler.get_crisis_response(
        crisis_level, 
        crisis_type,
        user_context
    )
    
    # Log the event
    crisis_handler.log_crisis_event(
        user_id=user_context.get("user_id", "anonymous") if user_context else "anonymous",
        crisis_level=crisis_level,
        crisis_type=crisis_type,
        message=validation_result.get("original_message", ""),
        action_taken="crisis_response_sent"
    )
    
    return response
