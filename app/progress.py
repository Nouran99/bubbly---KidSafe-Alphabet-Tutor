"""
Progress Tracking and Gamification Module
Tracks stars, badges, and achievements for motivation
Author: Nouran Darwish
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class BadgeType(Enum):
    FIRST_LETTER = "first_letter"
    FIVE_STREAK = "five_streak"
    TEN_LETTERS = "ten_letters"
    ALPHABET_HALF = "alphabet_half"
    ALPHABET_COMPLETE = "alphabet_complete"
    PERFECT_PRONUNCIATION = "perfect_pronunciation"
    HELPER = "helper"
    EXPLORER = "explorer"

@dataclass
class Badge:
    """Badge earned by child"""
    type: BadgeType
    name: str
    description: str
    icon: str
    earned_at: Optional[datetime] = None
    
@dataclass 
class Star:
    """Star earned for achievement"""
    letter: str
    confidence: float
    earned_at: datetime
    
class ProgressTracker:
    """
    Tracks child's learning progress with gamification elements
    """
    
    def __init__(self):
        self.stars: List[Star] = []
        self.badges: List[Badge] = []
        self.current_streak = 0
        self.best_streak = 0
        self.letters_mastered: List[str] = []
        self.total_attempts = 0
        self.perfect_pronunciations = 0
        
        # Define available badges
        self.available_badges = [
            Badge(
                BadgeType.FIRST_LETTER,
                "First Steps",
                "Learned your first letter!",
                "🌟"
            ),
            Badge(
                BadgeType.FIVE_STREAK,
                "On Fire!",
                "5 correct answers in a row!",
                "🔥"
            ),
            Badge(
                BadgeType.TEN_LETTERS,
                "Letter Expert",
                "Mastered 10 letters!",
                "🏆"
            ),
            Badge(
                BadgeType.ALPHABET_HALF,
                "Halfway Hero",
                "Learned half the alphabet!",
                "🎯"
            ),
            Badge(
                BadgeType.ALPHABET_COMPLETE,
                "Alphabet Champion",
                "Mastered the entire alphabet!",
                "👑"
            ),
            Badge(
                BadgeType.PERFECT_PRONUNCIATION,
                "Perfect Speaker",
                "Perfect pronunciation 10 times!",
                "🎤"
            ),
            Badge(
                BadgeType.HELPER,
                "Helpful Friend",
                "Used hints to learn better!",
                "💡"
            ),
            Badge(
                BadgeType.EXPLORER,
                "Letter Explorer",
                "Tried all different activities!",
                "🔍"
            )
        ]
        
    def award_star(self, letter: str, confidence: float) -> Optional[Star]:
        """
        Award a star for good performance
        Returns the star if awarded, None otherwise
        """
        if confidence >= 0.7:  # Threshold for earning a star
            star = Star(
                letter=letter,
                confidence=confidence,
                earned_at=datetime.now()
            )
            self.stars.append(star)
            
            # Update streak
            if confidence >= 0.8:
                self.current_streak += 1
                self.best_streak = max(self.best_streak, self.current_streak)
                
                if confidence >= 0.95:
                    self.perfect_pronunciations += 1
            else:
                self.current_streak = 0
                
            # Track mastered letters
            if letter not in self.letters_mastered and confidence >= 0.8:
                self.letters_mastered.append(letter)
                
            # Check for new badges
            self.check_badge_unlock()
            
            return star
        
        # Reset streak on failure
        if confidence < 0.6:
            self.current_streak = 0
            
        return None
        
    def check_badge_unlock(self) -> List[Badge]:
        """
        Check if any new badges should be unlocked
        Returns list of newly earned badges
        """
        new_badges = []
        
        # First Letter Badge
        if len(self.letters_mastered) >= 1:
            badge = self._award_badge(BadgeType.FIRST_LETTER)
            if badge:
                new_badges.append(badge)
                
        # Five Streak Badge
        if self.current_streak >= 5:
            badge = self._award_badge(BadgeType.FIVE_STREAK)
            if badge:
                new_badges.append(badge)
                
        # Ten Letters Badge
        if len(self.letters_mastered) >= 10:
            badge = self._award_badge(BadgeType.TEN_LETTERS)
            if badge:
                new_badges.append(badge)
                
        # Halfway Badge
        if len(self.letters_mastered) >= 13:
            badge = self._award_badge(BadgeType.ALPHABET_HALF)
            if badge:
                new_badges.append(badge)
                
        # Complete Alphabet Badge
        if len(self.letters_mastered) >= 26:
            badge = self._award_badge(BadgeType.ALPHABET_COMPLETE)
            if badge:
                new_badges.append(badge)
                
        # Perfect Pronunciation Badge
        if self.perfect_pronunciations >= 10:
            badge = self._award_badge(BadgeType.PERFECT_PRONUNCIATION)
            if badge:
                new_badges.append(badge)
                
        return new_badges
        
    def _award_badge(self, badge_type: BadgeType) -> Optional[Badge]:
        """
        Award a specific badge if not already earned
        """
        # Check if already earned
        if any(b.type == badge_type for b in self.badges):
            return None
            
        # Find and award the badge
        for badge in self.available_badges:
            if badge.type == badge_type:
                new_badge = Badge(
                    type=badge.type,
                    name=badge.name,
                    description=badge.description,
                    icon=badge.icon,
                    earned_at=datetime.now()
                )
                self.badges.append(new_badge)
                return new_badge
                
        return None
        
    def get_progress_summary(self) -> Dict:
        """
        Get comprehensive progress summary
        """
        return {
            "stars_earned": len(self.stars),
            "badges_earned": len(self.badges),
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "letters_mastered": len(self.letters_mastered),
            "mastered_list": self.letters_mastered,
            "perfect_pronunciations": self.perfect_pronunciations,
            "total_attempts": self.total_attempts,
            "recent_stars": [
                {
                    "letter": s.letter,
                    "confidence": f"{s.confidence:.0%}",
                    "time": s.earned_at.strftime("%H:%M")
                }
                for s in self.stars[-5:]  # Last 5 stars
            ],
            "badges": [
                {
                    "name": b.name,
                    "icon": b.icon,
                    "description": b.description
                }
                for b in self.badges
            ]
        }
        
    def get_motivational_message(self) -> str:
        """
        Generate motivational message based on progress
        """
        if self.current_streak >= 10:
            return "🌟 You're UNSTOPPABLE! Amazing streak!"
        elif self.current_streak >= 5:
            return "🔥 You're on fire! Keep it going!"
        elif self.current_streak >= 3:
            return "✨ Great job! You're doing wonderfully!"
        elif len(self.letters_mastered) >= 20:
            return "🏆 Almost there! You've learned so many letters!"
        elif len(self.letters_mastered) >= 10:
            return "🎯 Fantastic progress! You're a quick learner!"
        elif len(self.letters_mastered) >= 5:
            return "⭐ You're doing great! Keep learning!"
        else:
            return "🌈 Every letter is an adventure! Let's explore!"
            
    def get_html_display(self) -> str:
        """
        Generate HTML for progress display
        """
        summary = self.get_progress_summary()
        
        # Stars display
        stars_html = "⭐" * min(summary['stars_earned'], 10)
        if summary['stars_earned'] > 10:
            stars_html += f" +{summary['stars_earned'] - 10}"
            
        # Badges display
        badges_html = " ".join([b['icon'] for b in summary['badges'][:5]])
        
        # Streak display
        streak_html = ""
        if summary['current_streak'] > 0:
            streak_html = f"🔥 Streak: {summary['current_streak']}"
            
        html = f"""
        <div style='text-align: center; padding: 10px; background: rgba(255,255,255,0.9); border-radius: 10px;'>
            <div style='font-size: 24px; margin-bottom: 10px;'>
                {stars_html}
            </div>
            <div style='font-size: 20px; margin-bottom: 5px;'>
                {badges_html}
            </div>
            <div style='font-size: 16px; color: #ff6b6b;'>
                {streak_html}
            </div>
            <div style='font-size: 14px; margin-top: 10px; color: #666;'>
                Letters Mastered: {summary['letters_mastered']}/26
            </div>
            <div style='font-size: 16px; margin-top: 10px; color: #4a90e2; font-weight: bold;'>
                {self.get_motivational_message()}
            </div>
        </div>
        """
        
        return html
        
    def reset(self):
        """Reset all progress"""
        self.stars = []
        self.badges = []
        self.current_streak = 0
        self.best_streak = 0
        self.letters_mastered = []
        self.total_attempts = 0
        self.perfect_pronunciations = 0