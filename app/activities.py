"""
Interactive Activities and Games Module
Educational activities for alphabet learning
Author: Nouran Darwish
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ActivityType(Enum):
    REPEAT_AFTER_ME = "repeat_after_me"
    FIND_AN_OBJECT = "find_an_object"
    CHOOSE_THE_SOUND = "choose_the_sound"
    SHOW_THE_LETTER = "show_the_letter"
    LETTER_MATCHING = "letter_matching"
    RHYME_TIME = "rhyme_time"
    
@dataclass
class Activity:
    """Activity configuration"""
    type: ActivityType
    letter: str
    instruction: str
    options: List[str] = None
    correct_answer: str = None
    hints: List[str] = None
    
class AlphabetActivities:
    """
    Interactive activities for alphabet learning
    """
    
    def __init__(self, curriculum: Dict):
        self.curriculum = curriculum
        self.current_activity: Optional[Activity] = None
        self.activity_history: List[Activity] = []
        
    def repeat_after_me(self, letter: str) -> Activity:
        """
        Create a pronunciation practice activity
        """
        letter_info = self.curriculum['letters'].get(letter, {})
        phoneme = letter_info.get('phoneme', letter)
        sound_desc = letter_info.get('sound_description', '')
        
        instruction = f"Let's practice the letter {letter}! 🎤\n"
        instruction += f"Say '{letter}' - it sounds like {sound_desc}.\n"
        instruction += f"Listen carefully and repeat after me: '{letter}'... '{letter}'!"
        
        hints = [
            f"Remember, '{letter}' sounds like {phoneme}",
            f"Try saying it slowly: '{letter}'",
            f"Think of the word '{letter_info.get('example_words', [''])[0]}'"
        ]
        
        activity = Activity(
            type=ActivityType.REPEAT_AFTER_ME,
            letter=letter,
            instruction=instruction,
            correct_answer=letter,
            hints=hints
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def find_an_object(self, letter: str) -> Activity:
        """
        Create an object finding game
        """
        letter_info = self.curriculum['letters'].get(letter, {})
        mapped_object = letter_info.get('mapped_object', '')
        example_words = letter_info.get('example_words', [])
        
        instruction = f"🔍 Object Hunt Time! Find something that starts with '{letter}'!\n"
        instruction += f"Can you find: {', '.join(example_words[:3])}?\n"
        instruction += f"Look around you or show me a picture!"
        
        # Create options (correct + distractors)
        all_objects = []
        for l, info in self.curriculum['letters'].items():
            obj = info.get('mapped_object', '')
            if obj:
                all_objects.append(obj)
                
        # Select correct answer and distractors
        correct = mapped_object
        distractors = [obj for obj in all_objects if obj != correct]
        random.shuffle(distractors)
        options = [correct] + distractors[:3]
        random.shuffle(options)
        
        hints = [
            f"Look for something like a {mapped_object}",
            f"It starts with the '{letter}' sound",
            f"Think of {example_words[0] if example_words else 'something'} that begins with '{letter}'"
        ]
        
        activity = Activity(
            type=ActivityType.FIND_AN_OBJECT,
            letter=letter,
            instruction=instruction,
            options=options,
            correct_answer=correct,
            hints=hints
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def choose_the_sound(self, letter: str) -> Activity:
        """
        Create a sound discrimination activity
        """
        letter_info = self.curriculum['letters'].get(letter, {})
        confusions = letter_info.get('common_confusions', [])
        
        # Create sound options
        options = [letter]
        
        # Add confused letters if available
        if confusions:
            options.extend(confusions[:2])
            
        # Add random other letters
        other_letters = [l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
                        if l != letter and l not in confusions]
        random.shuffle(other_letters)
        
        while len(options) < 4:
            if other_letters:
                options.append(other_letters.pop())
                
        random.shuffle(options)
        
        instruction = f"🎵 Listen carefully! Which one sounds like '{letter}'?\n"
        instruction += f"I'll say each sound. Choose the right one!\n"
        instruction += f"Options: {', '.join(options)}"
        
        hints = [
            f"The '{letter}' sound is different from '{confusions[0] if confusions else 'other letters'}'",
            f"Listen for the '{letter_info.get('sound_description', letter)}' sound",
            f"Think of the word '{letter_info.get('example_words', [''])[0]}'"
        ]
        
        activity = Activity(
            type=ActivityType.CHOOSE_THE_SOUND,
            letter=letter,
            instruction=instruction,
            options=options,
            correct_answer=letter,
            hints=hints
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def show_the_letter(self, letter: str) -> Activity:
        """
        Create a letter recognition activity
        """
        instruction = f"📝 Can you show me the letter '{letter}'?\n"
        instruction += f"You can:\n"
        instruction += f"• Draw it in the air ✏️\n"
        instruction += f"• Write it on paper 📝\n"
        instruction += f"• Find it in a book 📚\n"
        instruction += f"• Show me with your hands 🤚"
        
        # Visual options (different representations)
        options = [
            f"Capital {letter}",
            f"Lowercase {letter.lower()}",
            f"Cursive {letter}",
            f"Block {letter}"
        ]
        
        hints = [
            f"The letter '{letter}' looks like this: {letter}",
            f"It's the {ord(letter) - ord('A') + 1}th letter of the alphabet",
            f"You see it in the word '{self.curriculum['letters'][letter].get('example_words', [''])[0]}'"
        ]
        
        activity = Activity(
            type=ActivityType.SHOW_THE_LETTER,
            letter=letter,
            instruction=instruction,
            options=options,
            correct_answer=letter,
            hints=hints
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def letter_matching(self, letter: str) -> Activity:
        """
        Create a letter-to-word matching game
        """
        letter_info = self.curriculum['letters'].get(letter, {})
        example_words = letter_info.get('example_words', [])
        
        # Get words from other letters
        other_words = []
        for l, info in self.curriculum['letters'].items():
            if l != letter:
                other_words.extend(info.get('example_words', [])[:1])
                
        # Create options
        correct_word = example_words[0] if example_words else f"{letter}-word"
        options = [correct_word] + random.sample(other_words, min(3, len(other_words)))
        random.shuffle(options)
        
        instruction = f"🎯 Which word starts with '{letter}'?\n"
        instruction += f"Choose the word that begins with the '{letter}' sound!\n"
        instruction += f"Options: {', '.join(options)}"
        
        hints = [
            f"Say each word slowly and listen to the first sound",
            f"'{correct_word}' starts with '{letter}'",
            f"The '{letter}' sound is like '{letter_info.get('sound_description', letter)}'"
        ]
        
        activity = Activity(
            type=ActivityType.LETTER_MATCHING,
            letter=letter,
            instruction=instruction,
            options=options,
            correct_answer=correct_word,
            hints=hints
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def rhyme_time(self, letter: str) -> Activity:
        """
        Create a rhyming activity with the letter sound
        """
        letter_info = self.curriculum['letters'].get(letter, {})
        
        # Simple rhymes for each letter
        rhymes = {
            'A': "A is for Apple, red and sweet, A yummy, crunchy treat to eat!",
            'B': "B is for Ball, bouncing high, Watch it bounce up to the sky!",
            'C': "C is for Cat, soft and furry, Chasing mice in such a hurry!",
            'D': "D is for Dog, wagging tail, Following you without fail!",
            'E': "E is for Elephant, big and gray, Splashing water all the day!",
            'F': "F is for Fish, swimming round, In the water, not a sound!",
            'G': "G is for Grapes, purple, green, The yummiest fruit you've ever seen!",
            'H': "H is for Hat, on your head, Keep you warm when you're in bed!",
            'I': "I is for Ice cream, cold and sweet, The perfect summer time treat!",
            'J': "J is for Jump, up so high, Try to touch the bright blue sky!",
            'K': "K is for Kite, flying free, High above the tallest tree!",
            'L': "L is for Lion, brave and strong, Roaring loud the whole day long!",
            'M': "M is for Mouse, small and quick, Finding cheese with just one lick!",
            'N': "N is for Nest, up in trees, Where baby birds sing in the breeze!",
            'O': "O is for Orange, round and bright, Full of juice, a tasty bite!",
            'P': "P is for Penguin, black and white, Sliding on ice, what a sight!",
            'Q': "Q is for Queen, with her crown, The fanciest lady in the town!",
            'R': "R is for Robot, beep beep boop, Moving in a metal group!",
            'S': "S is for Sun, shining bright, Giving us warmth and light!",
            'T': "T is for Tree, tall and green, The prettiest plant you've ever seen!",
            'U': "U is for Umbrella, keeping dry, When rain falls from the sky!",
            'V': "V is for Van, driving fast, Watch the scenery going past!",
            'W': "W is for Window, clear and bright, Letting in the morning light!",
            'X': "X is for X-ray, seeing through, Showing bones inside of you!",
            'Y': "Y is for Yo-yo, up and down, The coolest toy in town!",
            'Z': "Z is for Zebra, stripes so neat, Black and white from head to feet!"
        }
        
        rhyme = rhymes.get(letter, f"{letter} is special, {letter} is fun, Let's practice {letter} everyone!")
        
        instruction = f"🎵 Rhyme Time! Let's sing about '{letter}'!\n\n"
        instruction += rhyme + "\n\n"
        instruction += "Can you repeat this rhyme with me?"
        
        activity = Activity(
            type=ActivityType.RHYME_TIME,
            letter=letter,
            instruction=instruction,
            correct_answer=letter,
            hints=["Listen to the rhythm!", "Clap along with the rhyme!", "Make it fun with actions!"]
        )
        
        self.current_activity = activity
        self.activity_history.append(activity)
        return activity
        
    def get_random_activity(self, letter: str) -> Activity:
        """
        Get a random activity for the letter
        """
        activities = [
            self.repeat_after_me,
            self.find_an_object,
            self.choose_the_sound,
            self.show_the_letter,
            self.letter_matching,
            self.rhyme_time
        ]
        
        activity_func = random.choice(activities)
        return activity_func(letter)
        
    def check_answer(self, answer: str) -> Tuple[bool, str]:
        """
        Check if the answer is correct for current activity
        """
        if not self.current_activity:
            return False, "No active activity!"
            
        correct = self.current_activity.correct_answer
        is_correct = answer.lower() == correct.lower()
        
        if is_correct:
            responses = [
                "🎉 Excellent! That's absolutely right!",
                "⭐ Perfect! You're doing amazing!",
                "🌟 Wonderful! You got it!",
                "🏆 Great job! That's correct!",
                "✨ Fantastic! You're a star!"
            ]
            return True, random.choice(responses)
        else:
            hint = random.choice(self.current_activity.hints) if self.current_activity.hints else ""
            return False, f"Not quite! Let's try again. {hint}"
            
    def get_hint(self) -> str:
        """
        Get a hint for the current activity
        """
        if not self.current_activity or not self.current_activity.hints:
            return "Keep trying! You can do it!"
            
        return random.choice(self.current_activity.hints)