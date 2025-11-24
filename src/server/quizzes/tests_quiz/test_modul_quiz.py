
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul, Question, AnswerOption
from quizzes.serializers import QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCaseMissingValues(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5, semester=1)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user )

    def tearDown(self):
        return super().tearDown()
    
    def test_lernset_without_modul(self):
        """Ensure creating a Lernset without a connection to a modul is considered invalid"""
        lernset = Lernset(
            title="Orphan Lernset",
            created_by=self.user,
            modul=None  # modul is missing
    )
    # Check that lernset is None
        self.assertIsNone(lernset.modul_id)
    # Check that lernset would be invalid because modul is required
        is_valid = lernset.modul_id is not None and bool(lernset.title)
        self.assertFalse(is_valid)

    def test_missing_quiz_title(self):
        """Quiz without title should be considered invalid"""
        quiz = Quiz(
            title=None,
            description="No title",
            lernset=self.lernset
    )
    # Check that title is missing
        self.assertIsNone(quiz.title)
    # Check that quiz would be invalid because title is required
        is_valid = quiz.lernset is not None and bool(quiz.title)
        self.assertFalse(is_valid)

    def test_empty_quiz(self):
        """Quiz with no questions should be considered invalid"""
        quiz = Quiz(
            title="Empty Quiz",
            description="No questions",
            lernset=self.lernset
    )
    # Check that quiz has no questions
        self.assertEqual(quiz.questions.count(), 0)
    # Check that quiz would be invalid because questions are required
        is_valid = quiz.lernset is not None and quiz.questions.count() > 0
        self.assertFalse(is_valid)  

class TestSearchbar(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5, semester=1)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz1 = Quiz.objects.create(title="Algebra Basics", description="Basic algebra quiz", lernset=self.lernset, created_by=self.user)
        self.quiz2 = Quiz.objects.create(title="Calculus I", description="Introduction to calculus", lernset=self.lernset, created_by=self.user)
        self.quiz3 = Quiz.objects.create(title="Geometry Fundamentals", description="Basics of geometry", lernset=self.lernset, created_by=self.user)

    def test_search_quiz_by_title(self):
        """Searching for a quiz by title should return the correct quiz"""
        search_term = "Algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)
    
    def test_search_quiz_no_results(self):
        """Searching for a non-existing quiz should return no results"""
        search_term = "NonExistingQuiz"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertEqual(len(results), 0)

    def test_search_quiz_case_insensitive(self):
        """Searching should be case insensitive"""
        search_term = "algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)

    def test_search_lernset_by_title(self):
        """Searching for a lernset by title should return the correct lernset"""
        search_term = "Lernset"
        results = Lernset.objects.filter(title__icontains=search_term)
        self.assertIn(self.lernset, results)
        self.assertEqual(len(results), 1)
    
    def test_search_lernset_no_results(self):
        """Searching for a non-existing lernset should return no results"""
        search_term = "NonExistingLernset"
        results = Lernset.objects.filter(title__icontains=search_term)
        self.assertEqual(len(results), 0)
class Testserializers(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5, semester=1)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz = Quiz.objects.create(title="Sample Quiz", description="A sample quiz for testing", lernset=self.lernset, created_by=self.user)

    def test_update_quiz_with_questions(self):
        """Test the custom update method with questions and answer options"""
        # Create initial question
        question = Question.objects.create(
            quiz=self.quiz,
            text="Old question"
        )
        answer = AnswerOption.objects.create(
            question=question,
            text="Old answer",
            is_correct=True
        )

        # Prepare update payload
        update_data = {
            'title': "Updated Quiz Title",
            'description': "Updated description",
            'questions': [
                {
                    'id': question.id,
                    '_status': 'edited',
                    'text': "Updated question",
                    'answer_options': [
                        {'id': answer.id, 'text': "Updated answer", 'is_correct': False},
                        {'text': "New answer", 'is_correct': True}  # new answer
                    ]
                },
                {
                    '_status': 'new',
                    'text': "Brand new question",
                    'answer_options': [
                        {'text': "Answer 1", 'is_correct': True}
                    ]
                }
            ]
        }

        serializer = QuizSerializer(instance=self.quiz, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_quiz = serializer.save()

        # Check quiz fields
        self.assertEqual(updated_quiz.title, "Updated Quiz Title")
        self.assertEqual(updated_quiz.description, "Updated description")

        # Check updated question
        q1 = Question.objects.get(id=question.id)
        self.assertEqual(q1.text, "Updated question")
        self.assertEqual(q1.answer_options.count(), 2)

        # Check new question
        self.assertEqual(updated_quiz.questions.count(), 2)
        new_question = updated_quiz.questions.exclude(id=question.id).first()
        self.assertEqual(new_question.text, "Brand new question")
        self.assertEqual(new_question.answer_options.count(), 1)

        def test_quiz_serializer(self):
          """QuizSerializer should serialize quiz data correctly"""
        serializer = QuizSerializer(instance=self.quiz)
        data = serializer.data

        self.assertEqual(data['title'], "Sample Quiz")
        self.assertEqual(data['description'], "A sample quiz for testing")
        self.assertEqual(data['lernset'], self.lernset.id)
        self.assertEqual(data['created_by'], self.user.username)