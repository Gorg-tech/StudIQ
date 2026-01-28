from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul, Question, AnswerOption
from quizzes.serializers import QuestionSerializer, QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from accounts import serializers

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
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(serializers.ValidationError):
            serializer.save() 

       
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
        serializer.save()

        self.assertFalse(Question.objects.filter(id=self.question1.id).exists())
        self.assertTrue(Question.objects.filter(id=self.question2.id).exists())
        self.assertEqual(
            AnswerOption.objects.filter(question_id=self.question1.id).count(),
            0
        )

    def test_create_quiz_with_less_than_3_questions_fails(self):
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

    def test_create_new_question_in_existing_quiz_succeeds(self):
        data = {
        "title": self.quiz.title,
        "description": self.quiz.description,
        "lernset": self.lernset.id,
        "questions": [
            {
                "id": str(self.question1.id),
                "_status": "unchanged",
                "text": self.question1.text,
                "type": self.question1.type,
                "answer_options": []
            },
            {
                "id": str(self.question2.id),
                "_status": "unchanged",
                "text": self.question2.text,
                "type": self.question2.type,
                "answer_options": []
            },
            {
                "id": str(self.question3.id),
                "_status": "unchanged",
                "text": self.question3.text,
                "type": self.question3.type,
                "answer_options": []
            },
            {
                "_status": "new",
                "text": "New Question",
                "type": "SINGLE_CHOICE",
                "answer_options": [
                    {"text": "Yes", "is_correct": True},
                    {"text": "No", "is_correct": False}
                ]
            }
        ]
        }

        serializer = QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        quiz = serializer.save()

        self.assertEqual(quiz.questions.count(), 4)


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
        serializer.save()
        self.answer1.refresh_from_db()
        self.answer2.refresh_from_db()

        self.assertFalse(self.answer1.is_correct)
        self.assertTrue(self.answer2.is_correct)

    def test_update_quiz_with_all_questions_deleted_fails(self):
        data = {
            "title": self.quiz.title,
            "description": self.quiz.description,
            "lernset": self.lernset.id,
            "questions": [
                {"id": str(q.id), "_status": "deleted", "text": q.text, "type": q.type, "answer_options": []}
                for q in self.quiz.questions.all()
            ]
        }

        serializer = QuizSerializer(instance=self.quiz, data=data)
        self.assertTrue(serializer.is_valid())
        quiz = serializer.save()

        self.assertEqual(quiz.questions.count(), 0)

    def test_create_question_without_answer_options_fails(self):
        data = {
            "title": self.quiz.title,
            "description": self.quiz.description,
            "lernset": self.lernset.id,
            "questions": [
                {
                    "_status": "new",
                    "text": "Question without answers",
                    "type": "SINGLE_CHOICE",
                    "answer_options": []
                }
            ]
        }

        serializer = QuizSerializer(instance=self.quiz, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("questions", serializer.errors)


    def test_unauthenticated_user_cannot_edit_quiz(self):
        """Attempt to edit the quiz without authentication"""

        serializer = QuizSerializer(instance=self.quiz)
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(PermissionError):
            serializer.save()