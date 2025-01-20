import streamlit as st
import requests
from typing import Optional, List, Dict
from enum import Enum

class ConversationType(Enum):
    AI = "ai"
    CS = "cs"
    TAX_ADVISOR = "tax_advisor"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "How can we help you?",
        "avatar": "🤖",  # Will be replaced with Fiscozen logo
        "sender": "Fiscozen"
    })

# Setup recommender URL
RECOMMENDER_URL = "http://127.0.0.1:8000/recommend"

def get_recommendation(message: str) -> Dict:
    """Get recommendation from the service"""
    try:
        response = requests.post(
            RECOMMENDER_URL,
            json={
                "message": message,
                "user_id": st.session_state.get("user_id"),
                "context": {"history": st.session_state.messages}
            }
        )
        return response.json()
    except requests.RequestException:
        return {
            "response": "I'm having trouble connecting to the recommendation service. Please try again later.",
            "confidence": 0.0,
            "recommendations": None
        }

def update_conversation_type(conv_type: ConversationType):
    """Update the conversation type and visual indicators"""
    avatars = {
        ConversationType.AI: "🤖",
        ConversationType.CS: "👩‍💼",
        ConversationType.TAX_ADVISOR: "👨‍💼"
    }
    st.session_state.current_avatar = avatars[conv_type]
    st.session_state.current_sender = conv_type.value.title()

# Main UI
st.title("Fiscozen Chat")

# Chat container
chat_container = st.container()

# Display chat messages
for message in st.session_state.messages:
    with chat_container:
        with st.chat_message(
            message["role"],
            avatar=message.get("avatar", None)
        ):
            st.write(f"{message.get('sender', '')}: {message['content']}")
            if recommendations := message.get("recommendations"):
                st.info("Recommendations:")
                for rec in recommendations:
                    st.write(f"- {rec['text']}")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "sender": "You"
    })
    
    # Get recommendation
    recommendation = get_recommendation(prompt)
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": recommendation["response"],
        "avatar": "🤖",
        "sender": "Fiscozen",
        "recommendations": recommendation.get("recommendations")
    })
    
    # Rerun to update UI
    st.rerun() 