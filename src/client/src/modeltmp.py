import enum
import uuid
from sqlalchemy import (
    Column, String, Integer, DateTime, Date, Boolean, ForeignKey, Enum, Float, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Enums
class UserRole(enum.Enum):
    STUDENT = "STUDENT"
    MODERATOR = "MODERATOR"
    LECTURER = "LECTURER"

class QuizType(enum.Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FREITEXT = "FREITEXT"
    ZUORDNUNG = "ZUORDNUNG"

class DifficultyLevel(enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class QuizMode(enum.Enum):
    PRACTICE = "PRACTICE"
    SIMULATION = "SIMULATION"
    FLASHCARDS = "FLASHCARDS"
    CHALLENGE = "CHALLENGE"

# Modelle
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    registrationDate = Column(Date, default=datetime.utcnow)
    quiz_progress = relationship("QuizProgress", back_populates="user")
    learning_history = relationship("LearningHistory", uselist=False, back_populates="user")
    quizzes = relationship("Quiz", back_populates="creator")

class Modul(Base):
    __tablename__ = "module"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    description = Column(Text)
    topics = relationship("Topic", back_populates="modul")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    modul_id = Column(UUID(as_uuid=True), ForeignKey("module.id"))
    modul = relationship("Modul", back_populates="topics")
    quizzes = relationship("Quiz", back_populates="topic")

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    type = Column(Enum(QuizType), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    explanation = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)
    rating_score = Column(Integer, default=0)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"))
    topic = relationship("Topic", back_populates="quizzes")
    answer_options = relationship("AnswerOption", back_populates="quiz")
    quiz_progress = relationship("QuizProgress", back_populates="quiz")
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    creator = relationship("User", back_populates="quizzes")

class AnswerOption(Base):
    __tablename__ = "answer_options"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    isCorrect = Column(Boolean, nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", back_populates="answer_options")

class QuizProgress(Base):
    __tablename__ = "quiz_progress"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    correctAnswers = Column(Integer, default=0)
    wrongAnswers = Column(Integer, default=0)
    lastReviewed = Column(DateTime)
    strengthScore = Column(Float, default=0.0)
    user = relationship("User", back_populates="quiz_progress")
    quiz = relationship("Quiz", back_populates="quiz_progress")

class LearningHistory(Base):
    __tablename__ = "learning_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    iq_level = Column(Integer, default=0)
    correctAnswers = Column(Integer, default=0)
    wrongAnswers = Column(Integer, default=0)
    solvedQuizzes = Column(Integer, default=0)
    login_streak = Column(Integer, default=0)
    user = relationship("User", back_populates="learning_history")

class Badge(Base):
    __tablename__ = "badges"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    startTime = Column(DateTime, default=datetime.utcnow)
    endTime = Column(DateTime)
    score = Column(Integer, default=0)
    mode = Column(Enum(QuizMode), nullable=False)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    submittedAt = Column(Date, default=datetime.utcnow)

class StudyGroup(Base):
    __tablename__ = "study_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    createdAt = Column(Date, default=datetime.utcnow)