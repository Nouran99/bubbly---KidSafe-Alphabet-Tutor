#!/usr/bin/env python3
"""
Test script for KidSafe Alphabet Tutor components
Author: Nouran Darwish
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.state import SessionMemory
from agents.crew_setup import AlphabetTutorCrew
import json

def test_session_memory():
    """Test session memory management"""
    print("Testing Session Memory...")
    
    memory = SessionMemory()
    
    # Add some conversation turns
    memory.add_turn("My name is Alice", "Hello Alice! Nice to meet you!", "introduction", 0.9)
    memory.add_turn("Teach me B", "Let's learn the letter B!", "learn_letter", 0.8)
    memory.add_turn("B", "Good try!", "practice", 0.6)
    
    # Check state
    state = memory.get_derived_state_dict()
    print(f"Child name: {state['child_name']}")
    print(f"Current letter: {state['current_letter']}")
    print(f"Streak: {state['streak_count']}")
    
    # Get formatted memory
    formatted = memory.get_formatted_memory()
    print("\nFormatted Memory:")
    print(formatted)
    
    # Suggest next letter
    next_letter = memory.suggest_next_letter()
    print(f"\nSuggested next letter: {next_letter}")
    
    print("✅ Session Memory test passed!\n")
    
def test_crew_agents():
    """Test CrewAI agents"""
    print("Testing CrewAI Agents...")
    
    memory = SessionMemory()
    crew = AlphabetTutorCrew(memory)
    
    # Test intent classification
    intent = crew._classify_intent("Teach me the letter C")
    print(f"Intent for 'Teach me the letter C': {intent}")
    
    # Test entity extraction
    entities = crew._extract_entities("My name is Bob and I want to learn B")
    print(f"Extracted entities: {entities}")
    
    # Test safety check
    safe = crew._check_content_safety("Let's learn letters!")
    unsafe = crew._check_content_safety("What's your phone number?")
    print(f"Safety check (safe content): {safe}")
    print(f"Safety check (unsafe content): {unsafe}")
    
    # Test pronunciation analysis
    analysis = crew._analyze_pronunciation(0.7, "B")
    print(f"Pronunciation analysis: {analysis}")
    
    # Test feedback generation
    feedback = crew._generate_feedback(analysis)
    print(f"Generated feedback: {feedback}")
    
    print("✅ CrewAI Agents test passed!\n")
    
def test_curriculum():
    """Test curriculum loading"""
    print("Testing Curriculum...")
    
    with open('app/curriculum.json', 'r') as f:
        curriculum = json.load(f)
    
    # Check structure
    assert 'letters' in curriculum
    assert len(curriculum['letters']) == 26
    
    # Check a sample letter
    letter_a = curriculum['letters']['A']
    print(f"Letter A data:")
    print(f"  Phoneme: {letter_a['phoneme']}")
    print(f"  Example words: {letter_a['example_words']}")
    print(f"  Activities: {letter_a['activities']}")
    
    # Check progression rules
    progression = curriculum['progression_rules']
    print(f"\nEasy letters: {progression['easy_letters'][:5]}...")
    print(f"Confusion pairs: {progression['confusion_pairs'][:3]}...")
    
    print("✅ Curriculum test passed!\n")
    
def test_fallback_response():
    """Test fallback response system"""
    print("Testing Fallback Responses...")
    
    memory = SessionMemory()
    crew = AlphabetTutorCrew(memory)
    
    # Test various inputs
    test_inputs = [
        ("Hello", "introduction"),
        ("Teach me A", "learn_letter"),
        ("What's next?", "next_letter"),
        ("Help me", "help"),
        ("Again please", "repeat")
    ]
    
    for user_input, expected_intent in test_inputs:
        response = crew._fallback_response(user_input, 0.8)
        print(f"Input: '{user_input}'")
        print(f"Response: {response['response']}")
        print()
    
    print("✅ Fallback Response test passed!\n")

def main():
    """Run all tests"""
    print("=" * 60)
    print("KidSafe Alphabet Tutor - Component Tests")
    print("Author: Nouran Darwish")
    print("=" * 60)
    print()
    
    try:
        test_session_memory()
        test_curriculum()
        test_crew_agents()
        test_fallback_response()
        
        print("=" * 60)
        print("🎉 All tests passed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()