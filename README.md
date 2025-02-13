# Fiscozen ChatAI 🤖

An intelligent chat system that seamlessly transitions between AI assistance, customer service, and tax advisory services.

## 🌟 Features

- **Smart Routing**: Automatically directs conversations to:
  - AI Assistant for general queries
  - Customer Service representatives for complex cases
  - Tax Advisors for tax-related matters

- **Recommendation System**: Uses Microsoft's Recommenders library to:
  - Provide contextual responses
  - Suggest relevant information
  - Learn from conversation patterns

- **Modern UI**: Built with Streamlit for:
  - Clean, responsive interface
  - Real-time updates
  - Easy interaction

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone git@github.com:DavidVart/recommendations-project.git
cd recommendations-project
```

2. Set up the UI environment:
```bash
python -m venv venv-ui
source venv-ui/bin/activate  # On Windows: venv-ui\Scripts\activate
pip install -r requirements-ui.txt
pip install -e .
```

3. Set up the recommender service environment:
```bash
python -m venv venv-recommender
source venv-recommender/bin/activate  # On Windows: venv-recommender\Scripts\activate
pip install -r requirements-recommender.txt
pip install -e .
```

### Running the Application

1. Start the recommender service (in the recommender environment):
```bash
python run_recommender.py
```

2. In a new terminal, start the UI (in the UI environment):
```bash
python run_chat.py
```

The chat interface will be available at `http://localhost:8501`

## 🏗️ Project Structure

```
jorgelib/
├── ui/                 # Chat interface
├── recommender_service/# FastAPI service
├── models/            # Recommendation models
├── datasets/          # Data handling
├── routing/           # Conversation routing
└── chat/             # Core chat logic
```

## 🛠️ Development

- The project uses two separate environments to handle dependency conflicts
- UI runs on port 8501 (Streamlit)
- Recommender service runs on port 8000 (FastAPI)
- All code changes in `jorgelib/` are immediately reflected due to development installation

## 📚 Technologies Used

- [Streamlit](https://streamlit.io/) - UI Framework
- [Microsoft Recommenders](https://github.com/microsoft/recommenders) - Recommendation Engine
- [FastAPI](https://fastapi.tiangolo.com/) - API Framework
- [pandas](https://pandas.pydata.org/) - Data Processing

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
