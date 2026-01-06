from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul, Question, AnswerOption
from quizzes.serializers import QuestionSerializer, QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class TestCaseQuiz(TestCase):

    def setUp(self):
        # Shared user
        self.user = User.objects.create(username="testuser", password="testpass")

        # Shared module
        self.modul = Modul.objects.create(name="Test Modul", credits=5)

        # Shared lernset
        self.lernset = Lernset.objects.create(
            title="Test Lernset",
            modul=self.modul,
            created_by=self.user
        )

        # Shared quiz with 3 questions
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="A sample quiz for testing",
            lernset=self.lernset,
            created_by=self.user
        )

        # Questions for nested tests
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            text="Question 1",
            type="SINGLE_CHOICE"
        )
        self.question2 = Question.objects.create(
            quiz=self.quiz,
            text="Question 2",
            type="SINGLE_CHOICE"
        )
        self.question3 = Question.objects.create(
            quiz=self.quiz,
            text="Question 3",
            type="SINGLE_CHOICE"
        )

        # Answer options for question1
        self.answer1 = AnswerOption.objects.create(
            question=self.question1,
            text="Answer 1",
            is_correct=True
        )
        self.answer2 = AnswerOption.objects.create(
            question=self.question1,
            text="Answer 2",
            is_correct=False
        )

    def test_quiz_with_no_questions_fails(self):
        # Create a quiz with no questions
        data = {
            "title": "Empty Quiz",
            "description": "This quiz has no questions",
            "lernset": self.lernset.id,
            "questions": []
        }   
        serializer = QuizSerializer(data=data)
        self.assertFalse(serializer.is_valid())  

    #Quiz serializer
       
    def test_edit_answer_options_succeeds(self):
        data= {
            "title": self.quiz.title,
            "description": self.quiz.description,
            "lernset": self.lernset.id,
            "questions": [
                {
                    "id": self.question1.id,
                    "_status": "edited",
                    "text": self.question1.text,
                    "type": self.question1.type,
                    "answer_options": [
                        {
                            "id": str(self.answer1.id),
                            "text": "Updated Answer 1",
                            "is_correct": True,
                            "_status": "edited"
                        },
                        {
                            "id": str(self.answer2.id),
                            "text": "Updated Answer 2",
                            "is_correct": False,
                            "_status": "edited"
                        }
                    ]
                }
            ]
        }

        serializer=QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save()


        self.answer1.refresh_from_db()
        self.answer2.refresh_from_db()

        self.assertEqual(self.answer1.text, "Updated Answer 1")
        self.assertEqual(self.answer2.text, "Updated Answer 2") 

    def test_delete_question_removes_answer_options(self):
        # Prepare data to delete question1
        data = {
        "title": self.quiz.title,
        "description": self.quiz.description,
        "lernset": self.lernset.id,
        "questions": [
            {
                "id": str(self.question1.id),
                "_status": "deleted",
                "text": self.question1.text,
                "type": self.question1.type,
                "answer_options": []
            },
            {
                "id": str(self.question2.id),
                "_status": "unchanged",
                "text": self.question2.text,
                "type": self.question2.type,
                "answer_options": [
                    {
                        "id": str(self.question2.answer_options.first().id) if self.question2.answer_options.exists() else None,
                        "text": "Answer B",
                        "is_correct": True,
                        "_status": "unchanged"
                    }
                ]
            }
        ]
    }

        serializer = QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save()

        # Question1 should be gone
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.question1.id)

        # Question2 should still exist
        self.assertTrue(Question.objects.filter(id=self.question2.id).exists())

        # All answer options for question1 are gone
        self.assertEqual(AnswerOption.objects.filter(question=self.question1).count(), 0)

    
    def test_create_quiz_with_valid_data_succeeds(self):
        data = {
            "title": "New Quiz",
            "description": "A new quiz",
            "created_by_id": self.user.id,
            "lernset": self.lernset.id,
            "questions": [
                {
                    "text": "New Question 1",
                    "type": "SINGLE_CHOICE",
                    "_status": "new",
                    "answer_options": [
                        {
                            "text": "New Answer 1",
                            "is_correct": True,
                            "_status": "new"
                        },
                        {
                            "text": "New Answer 2",     
                            "is_correct": False,
                            "_status": "new"
                        }
                    ]
                },
                {
                    "text": "New Question 2",
                    "type": "SINGLE_CHOICE",
                    "_status": "new",
                    "answer_options": [
                        {
                            "text": "New Answer 1",
                            "is_correct": True,
                            "_status": "new"
                        },
                        {
                            "text": "New Answer 2",     
                            "is_correct": False,
                            "_status": "new"
                        }
                    ]
                },
                {
                    "text": "New Question 3",
                    "type": "SINGLE_CHOICE",
                    "_status": "new",
                    "answer_options": [
                        {
                            "text": "New Answer 1",
                            "is_correct": True,
                            "_status": "new"
                        },
                        {
                            "text": "New Answer 2",     
                            "is_correct": False,
                            "_status": "new"
                        }
                    ]
                }
            ]
        }
        serializer = QuizSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save(created_by=self.user)
        self.assertEqual(quiz.title, "New Quiz")
        self.assertEqual(quiz.description, "A new quiz")
        self.assertEqual(quiz.lernset, self.lernset)

    def test_create_new_question_in_existing_quiz_succeeds(self):
        data = {
        "title": self.quiz.title,
        "description": self.quiz.description,
        "lernset": self.lernset.id,
        "questions": [
            {
                "text": "New Question",
                "type": "SINGLE_CHOICE",
                "_status": "new",
                "answer_options": [
                    {
                        "text": "New Answer 1",
                        "is_correct": True,
                        "_status": "new"
                    },
                    {
                        "text": "New Answer 2",
                        "is_correct": False,
                        "_status": "new"
                    }
                ]
            }
        ]
    }   
        
        serializer=QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save()
        self.assertEqual(quiz.questions.count(), 4)
        new_question = quiz.questions.get(text="New Question")

    def test_correct_answer_changeable_succeeds(self):
        data = {
        "title": self.quiz.title,
        "description": self.quiz.description,
        "lernset": self.lernset.id,
        "questions": [
            {
                "id": str(self.question1.id),
                "_status": "edited",
                "text": self.question1.text,
                "type": self.question1.type,
                "answer_options": [
                    {
                        "id": str(self.answer1.id),
                        "text": "Updated Answer 1",
                        "is_correct": False,
                        "_status": "edited"
                    },
                    {
                        "id": str(self.answer2.id),
                        "text": "Updated Answer 2",
                        "is_correct": True,
                        "_status": "edited"
                    }
                ]
            }
        ]
    }
        serializer=QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save()
        self.answer1.refresh_from_db()
        self.answer2.refresh_from_db()

        updated_answer1 = AnswerOption.objects.get(id=self.answer1.id)
        updated_answer2 = AnswerOption.objects.get(id=self.answer2.id)
        self.assertFalse(updated_answer1.is_correct)
        self.assertTrue(updated_answer2.is_correct)


class TestSearchbar(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz1 = Quiz.objects.create(title="Algebra Basics", description="Basic algebra quiz", lernset=self.lernset, created_by=self.user)
        self.quiz2 = Quiz.objects.create(title="Calculus I", description="Introduction to calculus", lernset=self.lernset, created_by=self.user)
        self.quiz3 = Quiz.objects.create(title="Geometry Fundamentals", description="Basics of geometry", lernset=self.lernset, created_by=self.user)

    def test_search_quiz_by_title_suceeds(self):
        """Searching for a quiz by title should return the correct quiz"""
        search_term = "Algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)
    
    def test_search_nonexisting_quiz_fails(self):
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
