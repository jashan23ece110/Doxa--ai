"""Learning package initialization."""
from app.core.learning.learning_metrics import learning_metrics_tracker, LearningMetricsTracker
from app.core.learning.feedback_engine import feedback_engine, FeedbackEngine, FeedbackType, UserFeedbackItem
from app.core.learning.learning_repository import learning_repository, JSONLearningRepository, LearningRecord
from app.core.learning.prompt_optimizer import prompt_optimizer, PromptOptimizer, PromptOptimizationProposal
from app.core.learning.retrieval_optimizer import retrieval_optimizer, RetrievalOptimizer
from app.core.learning.tool_learning import tool_learning_engine, ToolLearningEngine, ToolExecutionStats
from app.core.learning.conversation_learning import conversation_learning, ConversationLearning
from app.core.learning.knowledge_evolution import knowledge_evolution_engine, KnowledgeEvolutionEngine
from app.core.learning.learning_engine import continuous_learning_engine, ContinuousLearningEngine

__all__ = [
    "learning_metrics_tracker",
    "LearningMetricsTracker",
    "feedback_engine",
    "FeedbackEngine",
    "FeedbackType",
    "UserFeedbackItem",
    "learning_repository",
    "JSONLearningRepository",
    "LearningRecord",
    "prompt_optimizer",
    "PromptOptimizer",
    "PromptOptimizationProposal",
    "retrieval_optimizer",
    "RetrievalOptimizer",
    "tool_learning_engine",
    "ToolLearningEngine",
    "ToolExecutionStats",
    "conversation_learning",
    "ConversationLearning",
    "knowledge_evolution_engine",
    "KnowledgeEvolutionEngine",
    "continuous_learning_engine",
    "ContinuousLearningEngine",
]
