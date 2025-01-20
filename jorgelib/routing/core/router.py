from enum import Enum
from typing import Optional
import re

class ConversationType(Enum):
    AI = "ai"
    CS = "cs"
    TAX_ADVISOR = "tax_advisor"

class ConversationRouter:
    def __init__(self):
        self.current_type = ConversationType.AI
        self.tax_keywords = ['tax', 'taxes', 'taxation', 'advisor', 'consultation']
        self.confidence_threshold = 0.7
        
    def determine_route(self, message: str, confidence_score: float) -> ConversationType:
        """
        Determines if conversation should be routed to CS or Tax Advisor
        Args:
            message: User's message
            confidence_score: AI's confidence in handling the query
        """
        # Check for tax-related keywords
        if any(keyword in message.lower() for keyword in self.tax_keywords):
            return ConversationType.TAX_ADVISOR
            
        # Route to CS if confidence is low
        if confidence_score < self.confidence_threshold:
            return ConversationType.CS
            
        return ConversationType.AI 