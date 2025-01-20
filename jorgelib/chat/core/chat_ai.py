from typing import Optional, List, Dict
from ...routing.core.router import ConversationType, ConversationRouter
from ...models.conversation_recommender import ConversationRecommender
from ...datasets.conversation_data import ConversationDataset, ConversationTurn

class ChatAI:
    def __init__(self, dataset: Optional[ConversationDataset] = None):
        self.conversation_history: List[ConversationTurn] = []
        self.dataset = dataset or ConversationDataset()
        self.recommender = ConversationRecommender(self.dataset)
        self.router = ConversationRouter()
        
    def start_conversation(self) -> str:
        """Initiates conversation with welcome message"""
        self.conversation_history = []
        return "How can we help you?"
        
    def process_message(self, message: str) -> dict:
        """
        Process user message and decide next action
        Returns:
            dict with keys:
            - response: str
            - action: str ('continue', 'cs_handoff', 'tax_advisor')
            - recommendations: List[dict] optional
        """
        # Get recommendation
        recommendation = self.recommender.get_response(message)
        
        # Determine routing
        route = self.router.determine_route(
            message=message,
            confidence_score=recommendation['confidence']
        )
        
        # Prepare response based on routing
        response = {
            'response': recommendation['response'],
            'action': route.value,
            'recommendations': recommendation['recommendations']
        }
        
        # Store conversation turn
        self.conversation_history.append(
            ConversationTurn(
                user_message=message,
                system_response=response['response'],
                action_taken=route.value,
                confidence_score=recommendation['confidence'],
                recommendations=recommendation['recommendations']
            )
        )
        
        return response 