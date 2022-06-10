import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test import Client

from .models import Question, Choice

POLLS_INDEX = reverse('polls:index')

class QuestionModelTests(TestCase):

    def test_was_published_with_future_question(self):
        """tests if the database element was created in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """check if was_published_recently returns False for questions
        whose pub_date is older than 1 day"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_with_recent_question(self):
        """Test if was_published_recently returns True for questions
        whose pub_date is less than 1 day"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
     in the past, positive for questions that have yet not be bublished)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(choice_text, question):
    """Create Choice for a question"""
    return question.choice_set.create(choice_text=choice_text,
                                votes=0)


class QuestionIndexViewTest(TestCase):

    def setup(self):
        self.client = Client()

    def test_no_questions(self):
        """If no questions exist, message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_empty_choices(self):
        """test if question with no choices return 404"""
        question = create_question(question_text="Some question", days=0)
        response = self.client.get(POLLS_INDEX)
        self.assertEqual(response.status_code, 404)


    def test_question_with_choice(self):
        """test if question with any choice will be displayed"""
        question = create_question(question_text="Some question", days=0)
        choice = create_choice(choice_text="Some choice", question=question)
        response = self.client.get(POLLS_INDEX)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the
         index page"""
        question = create_question(question_text='Past question', days=-30)
        choice = create_choice(choice_text="generic choice",
                                question=question)
        response = self.client.get(POLLS_INDEX)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
         )

    def test_future_question(self):
        """test if question with future question date are not displayed"""
        question = create_question(question_text="Future question", days=30)
        response = self.client.get(POLLS_INDEX)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """test if both future and past questions onley past are displayed"""
        past_one = create_question(question_text="Past question.", days=-10)
        future_one = create_question(question_text="Future question.", days=30)
        response = self.client.get(POLLS_INDEX)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_one],
        )

    def test_two_past_questions(self):
        """test if both past quesions is displayed"""
        question1 = create_question(question_text="past question1.", days=-30)
        question2 = create_question(question_text="past question2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )
class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """test if detail view of nor published future question gives 404"""
        future_question = create_question(question_text='Future question.',
                                            days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays
        the question text"""
        past_question = create_question(question_text='Past question',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionReasultsViewTest(TestCase):

    def test_future_question(self):
        """test if results view for not published questions gives 404 after
        directly passing the addres"""
        future_question = create_question(question_text="Future_question.",
                                            days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """test if reasult view for publised question is visible"""
        past_question = create_question(question_text="Past question.",
                                        days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
