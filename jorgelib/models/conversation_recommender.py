from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from recommenders.models.deeprec.models.base_model import BaseModel
from recommenders.models.deeprec.deeprec_utils import prepare_hparams
from recommenders.models.deeprec.io.sequential_iterator import SequentialIterator
from recommenders.datasets.download_utils import maybe_download
from ..datasets.conversation_data import ConversationTurn, ConversationDataset

class ConversationRecommender:
    def __init__(self, dataset: ConversationDataset):
        self.dataset = dataset
        self.confidence_threshold = 0.7
        self._initialize_recommender()
        
    def _initialize_recommender(self):
        """Initialize the deep learning recommender model"""
        # Convert conversations to user-item interaction format
        self.interactions_df = self._prepare_interaction_data()
        
        # Setup model parameters
        self.hparams = prepare_hparams(
            "nrms",  # Neural Recommendation Model with Self-Attention
            embed_size=100,
            attention_size=100,
            max_seq_length=50,
            need_sample=True,
            learning_rate=0.001
        )
        
        # Initialize model
        self.model = BaseModel(self.hparams, BaseModel._init_model)
        
    def _prepare_interaction_data(self) -> pd.DataFrame:
        """Convert conversation data to user-item interactions"""
        interactions = []
        
        for conv_id, conv in enumerate(self.dataset.conversations):
            for turn_id, turn in enumerate(conv):
                interactions.append({
                    'userID': f'user_{conv_id}',
                    'itemID': f'msg_{turn_id}',
                    'rating': turn.confidence_score,
                    'timestamp': turn_id,
                    'message': turn.user_message,
                    'response': turn.system_response
                })
        
        return pd.DataFrame(interactions)
    
    def get_response(self, message: str) -> Dict:
        """
        Get recommended response based on message context using deep recommender
        Returns:
            dict containing:
            - response: str
            - confidence: float
            - recommendations: List[Dict] optional
        """
        if not self.dataset.conversations:
            return {
                'response': "I'm not sure how to help with that. Let me connect you with a customer service representative.",
                'confidence': 0.0,
                'recommendations': None
            }
            
        # Get similar messages using recommender
        message_embedding = self.model.run_embedding(message)
        similar_indices = self._get_similar_messages(message_embedding)
        
        if not similar_indices:
            return {
                'response': "I'm not sure how to help with that. Let me connect you with a customer service representative.",
                'confidence': 0.0,
                'recommendations': None
            }
        
        # Get best matching response
        best_match = self.interactions_df.iloc[similar_indices[0]]
        
        # Get related recommendations
        recommendations = self._get_recommendations(best_match['userID'])
        
        return {
            'response': best_match['response'],
            'confidence': float(best_match['rating']),
            'recommendations': recommendations
        }
        
    def _get_similar_messages(self, query_embedding, top_k: int = 5) -> List[int]:
        """Find similar messages using embeddings"""
        # Get embeddings for all messages
        message_embeddings = np.array([
            self.model.run_embedding(msg) 
            for msg in self.interactions_df['message']
        ])
        
        # Calculate cosine similarities
        similarities = np.dot(message_embeddings, query_embedding) / (
            np.linalg.norm(message_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        return np.argsort(similarities)[-top_k:][::-1]
        
    def _get_recommendations(self, user_id: str, top_k: int = 3) -> List[Dict]:
        """Get personalized recommendations for user"""
        # Use model to predict next items
        user_history = self.interactions_df[
            self.interactions_df['userID'] == user_id
        ]['itemID'].tolist()
        
        predictions = self.model.predict(user_history)
        top_items = np.argsort(predictions)[-top_k:][::-1]
        
        return [
            {
                'item_id': self.interactions_df.iloc[idx]['itemID'],
                'score': float(predictions[idx]),
                'response': self.interactions_df.iloc[idx]['response']
            }
            for idx in top_items
        ] 