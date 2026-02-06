"""
Example Usage: Ethics Configuration System
Shows how to use ethics_config.yaml in your code
"""
import asyncio
from ethics_config_loader import load_ethics_config


async def example_usage():
    """Demonstrate how to use ethics configuration"""
    
    # Load configuration
    config = load_ethics_config()
    
    print(f"📋 Ethics Config v{config.get_version()}")
    print(f"Last Updated: {config.get_last_updated()}\n")
    
    # ========== Crisis Detection Example ==========
    print("=" * 60)
    print("CRISIS DETECTION")
    print("=" * 60)
    
    # Get crisis keywords
    critical_keywords = config.get_crisis_keywords('critical')
    print(f"\n🚨 Critical Keywords ({len(critical_keywords)}):")
    print(f"  {', '.join(critical_keywords[:5])}...")
    
    # Get hotlines
    primary_hotline = config.get_hotline('primary')
    print(f"\n📞 Primary Hotline:")
    print(f"  {primary_hotline['name']}: {primary_hotline['number']}")
    print(f"  Available: {primary_hotline['availability']}")
    
    # Get crisis response template
    crisis_template = config.get_crisis_response_template()
    print(f"\n💬 Crisis Response Template:")
    print(f"  {crisis_template[:100]}...")
    
    # ========== Prohibited Patterns Example ==========
    print("\n" + "=" * 60)
    print("PROHIBITED PATTERNS")
    print("=" * 60)
    
    # Get diagnosis patterns
    diagnosis_patterns = config.get_prohibited_patterns('diagnosis')
    print(f"\n❌ Diagnosis Patterns ({len(diagnosis_patterns)}):")
    for pattern in diagnosis_patterns[:3]:
        print(f"  - {pattern}")
    
    # Get conditions AI cannot diagnose
    conditions = config.get_prohibited_conditions()
    print(f"\n🏥 Conditions AI Cannot Diagnose ({len(conditions)}):")
    print(f"  {', '.join(conditions[:5])}...")
    
    # ========== Disclaimers Example ==========
    print("\n" + "=" * 60)
    print("DISCLAIMERS")
    print("=" * 60)
    
    # Get conversation start disclaimer
    start_disclaimer = config.get_disclaimer('conversation_start')
    print(f"\n💬 Conversation Start:")
    print(f'  "{start_disclaimer}"')
    
    # Get user agreement points
    agreement_points = config.get_user_agreement_points()
    print(f"\n📜 User Agreement ({len(agreement_points)} points):")
    for i, point in enumerate(agreement_points[:3], 1):
        print(f"  {i}. {point}")
    
    # ========== Cultural Settings Example ==========
    print("\n" + "=" * 60)
    print("CULTURAL SETTINGS")
    print("=" * 60)
    
    # Get derogatory terms to avoid
    derogatory = config.get_derogatory_terms()
    print(f"\n🚫 Derogatory Terms to Avoid:")
    print(f"  {', '.join(derogatory)}")
    
    # Get language style
    lang_style = config.get_language_style()
    print(f"\n🌐 Language Style: {lang_style}")
    
    # ========== Age Settings Example ==========
    print("\n" + "=" * 60)
    print("AGE SETTINGS")
    print("=" * 60)
    
    min_age = config.get_minimum_age()
    print(f"\n👶 Minimum Age: {min_age}")
    
    # Check age appropriateness
    test_ages = [10, 15, 20]
    for age in test_ages:
        appropriate = config.is_age_appropriate(age)
        status = "✅ Allowed" if appropriate else "❌ Blocked"
        print(f"  Age {age}: {status}")
        
        if appropriate and age < 18:
            restrictions = config.get_age_restrictions(age)
            print(f"    → {restrictions}")
    
    # ========== Personality Settings Example ==========
    print("\n" + "=" * 60)
    print("PERSONALITY SETTINGS")
    print("=" * 60)
    
    personality = config.get_personality_traits()
    tone = personality.get('tone', {})
    print(f"\n🎭 AI Tone:")
    for key, value in tone.items():
        print(f"  {key}: {value}")
    
    response_structure = config.get_response_structure()
    print(f"\n📝 Response Structure:")
    for key, value in response_structure.items():
        print(f"  {key}: {value}")
    
    # ========== Professional Referral Example ==========
    print("\n" + "=" * 60)
    print("PROFESSIONAL REFERRAL")
    print("=" * 60)
    
    referral_criteria = config.get_referral_criteria()
    print(f"\n🏥 When to Refer ({len(referral_criteria)} criteria):")
    for i, criterion in enumerate(referral_criteria[:5], 1):
        print(f"  {i}. {criterion}")
    
    # ========== Data Protection Example ==========
    print("\n" + "=" * 60)
    print("DATA PROTECTION (UU PDP)")
    print("=" * 60)
    
    uu_pdp = config.is_uu_pdp_compliant()
    print(f"\n🔒 UU PDP Compliant: {uu_pdp}")
    
    principles = config.get_data_protection_principles()
    print(f"\n📋 Data Protection Principles:")
    for key, value in principles.items():
        print(f"  {key}: {value}")
    
    user_rights = config.get_user_data_rights()
    print(f"\n👤 User Data Rights:")
    for key, value in user_rights.items():
        print(f"  {key}: {value}")
    
    # ========== Quality Assurance Example ==========
    print("\n" + "=" * 60)
    print("QUALITY ASSURANCE")
    print("=" * 60)
    
    qa_checklist = config.get_qa_checklist()
    print(f"\n✅ Pre-Response Checklist ({len(qa_checklist)} items):")
    for item in qa_checklist:
        print(f"  - [ ] {item}")
    
    review_triggers = config.get_human_review_triggers()
    print(f"\n🚨 Human Review Triggers ({len(review_triggers)}):")
    for trigger in review_triggers:
        print(f"  - {trigger}")
    
    # ========== Implementation Status ==========
    print("\n" + "=" * 60)
    print("IMPLEMENTATION STATUS")
    print("=" * 60)
    
    status = config.get_implementation_status()
    print(f"\n📊 Implementation Checklist:")
    for key, value in status.items():
        icon = "✅" if value else "⏳"
        print(f"  {icon} {key.replace('_', ' ').title()}")


# ========== Integration Example ==========

async def example_chat_with_ethics():
    """Example: Using ethics config in chat endpoint"""
    config = load_ethics_config()
    
    # Simulate user message
    user_message = "Saya ingin bunuh diri"
    
    print("\n" + "=" * 60)
    print("CHAT INTEGRATION EXAMPLE")
    print("=" * 60)
    print(f"\nUser: {user_message}")
    
    # Check if message contains crisis keywords
    all_keywords = config.get_all_crisis_keywords()
    detected_keywords = [kw for kw in all_keywords if kw in user_message.lower()]
    
    if detected_keywords:
        print(f"\n🚨 CRISIS DETECTED!")
        print(f"Keywords: {detected_keywords}")
        
        # Get crisis response
        crisis_response = config.get_crisis_response_template()
        print(f"\n💬 Auto Response:")
        print(crisis_response)
        
        # Get hotlines
        print(f"\n📞 Hotlines Provided:")
        for hotline_type, info in config.get_all_hotlines().items():
            print(f"  - {info['name']}: {info['number']}")
    else:
        print(f"\n✅ No crisis detected, proceeding with normal AI response")


async def example_output_validation():
    """Example: Validate AI output against ethics rules"""
    config = load_ethics_config()
    
    print("\n" + "=" * 60)
    print("OUTPUT VALIDATION EXAMPLE")
    print("=" * 60)
    
    # Test responses
    test_responses = [
        "Kamu menderita depresi mayor, harus minum antidepresan",  # BAD
        "Wajar merasa sedih. Mau cerita lebih lanjut?",           # GOOD
        "Kamu tidak perlu psikolog, aku aja cukup",                # BAD
        "Gejala yang kamu alami sebaiknya dibahas dengan profesional" # GOOD
    ]
    
    all_prohibited = config.get_prohibited_patterns()
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n{i}. Testing: \"{response[:50]}...\"")
        
        # Check against prohibited patterns
        violations = [p for p in all_prohibited if p.lower() in response.lower()]
        
        if violations:
            print(f"   ❌ BLOCKED - Violations: {violations}")
        else:
            print(f"   ✅ PASSED - No ethics violations")


if __name__ == "__main__":
    print("\n" + "🎯" * 30)
    print("LENTERA ETHICS CONFIGURATION SYSTEM")
    print("🎯" * 30 + "\n")
    
    # Run examples
    asyncio.run(example_usage())
    asyncio.run(example_chat_with_ethics())
    asyncio.run(example_output_validation())
    
    print("\n" + "=" * 60)
    print("✅ Examples completed successfully!")
    print("=" * 60)
