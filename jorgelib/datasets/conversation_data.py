from typing import List, Dict, Optional
from dataclasses import dataclass
import pandas as pd
from recommenders.utils.constants import DEFAULT_USER_COL, DEFAULT_ITEM_COL, DEFAULT_RATING_COL
from recommenders.datasets import download_path
from recommenders.models.deeprec.deeprec_utils import download_deeprec_resources

@dataclass
class ConversationTurn:
    user_message: str
    system_response: str
    action_taken: str  # 'continue', 'cs_handoff', 'tax_advisor'
    confidence_score: float
    recommendations: Optional[List[Dict]] = None

class ConversationDataset:
    def __init__(self):
        self.conversations: List[List[ConversationTurn]] = []
        self._download_resources()
        
    def _download_resources(self):
        """Download necessary resources for the recommender"""
        self.resource_path = download_deeprec_resources(
            'nrms',
            download_path.DEFAULT_DOWNLOAD_PATH
        )
    
    def add_conversation(self, conversation: List[ConversationTurn]):
        """Add a complete conversation to the dataset"""
        self.conversations.append(conversation)
    
    def get_similar_conversations(self, query: str, top_k: int = 5) -> List[List[ConversationTurn]]:
        """
        Retrieve top-k similar conversations based on query
        Note: This is now handled by the recommender model directly
        """
        return []
        
    def to_pandas(self) -> pd.DataFrame:
        """Convert dataset to pandas DataFrame for recommender system"""
        interactions = []
        
        for conv_id, conv in enumerate(self.conversations):
            for turn_id, turn in enumerate(conv):
                interactions.append({
                    DEFAULT_USER_COL: f'user_{conv_id}',
                    DEFAULT_ITEM_COL: f'msg_{turn_id}',
                    DEFAULT_RATING_COL: turn.confidence_score,
                    'timestamp': turn_id,
                    'message': turn.user_message,
                    'response': turn.system_response
                })
        
        return pd.DataFrame(interactions) 