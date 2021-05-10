from npdapp.settings import DATA_DEBUG_MODE, BASE_DIR

import io
import datetime
import uuid
import validate_email

#from jsonfield import JSONField

import json
import os

import requests
from requests.exceptions import ConnectionError
from datetime import datetime

import pandas as pd
from pandas.io.json import json_normalize

from django_pandas.io import read_frame
from django.db.models import F

from django.db import models
from django.conf import settings


from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from initiatives.models import User

from surveys.managers import QuestionManager, SurveyManager

from .utils import clean_input_list


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def f7(seq):  # UNIQUE PRESERVE ORDER!!
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def default_properties():
    return {
        "foo": "bar",
        "lorem": "ipsum"
    }


def default_duplicatescheck():
    return ['EMAIL']


def checkbox_q_default():
    return {
        "question_options": [
            {"id": 1, "subId": 311, "value": "Ford",
                "checked": "false", "edit": "false"},
            {"id": 2, "subId": 141, "value": "Vauxhall",
                "checked": "false", "edit": "false"},
            {"id": 3, "subId": 121, "value": "Volkswagen",
                "checked": "false", "edit": "false"},
            {"id": 4, "subId": 161, "value": "Nissan",
                "checked": "false", "edit": "false"},
            {"id": 5, "subId": 921, "value": "Audi",
                "checked": "false", "edit": "false"}
        ],
        "selected": [
            #{ "id":1,"subId":311, "value": "Ford", "checked": "false", "edit": "false" },
            #{ "id":3,"subId":121, "value": "Volkswagen", "checked": "false", "edit": "false" }
        ],
        "question_answers": []
    }


def emotion_q_default():
    return {
        "current_increment": 1,
        "stars_rating": 7,
        "answer": 0,
        "question_answers": []
    }


def rateimage_q_default():
    return {
        "current_increment": 1,
        "stars_rating": 9,
        "answer": 0,
        "question_answers": []
    }


def select_q_default():
    return {
        "question_options": [
            {"id": 1, "subId": "The Width Of A Circle",
                "value": "David Bowie", "checked": "false", "edit": "false"},
            {"id": 2, "subId": "Dear Mama", "value": "2Pac",
                "checked": "false", "edit": "false"},
            {"id": 3, "subId": "As", "value": "Stevie Wonder",
                "checked": "false", "edit": "false"},
            {"id": 4, "subId": "Nothing Compares 2 U",
                "value": "Sinéad O’Connor", "checked": "false", "edit": "false"},
            {"id": 5, "subId": "Clean", "value": "Depeche Mode",
                "checked": "false", "edit": "false"}
        ],
        "selected": "",
        "question_answers": []
    }


def mocktest_conjoint_q_pairs_one():

    MOCK_DATA_DIR = os.path.join(BASE_DIR, 'mockdata', 'caone_answers')
    mock_file = os.path.join(MOCK_DATA_DIR, 'mock_cars_full_01.json')
    #mock_file = os.path.join(MOCK_DATA_DIR, 'mock_rice_full_01.json')
    #mock_file = os.path.join(MOCK_DATA_DIR, 'mock_chocolate_adjusted_price_01.json')
    #mock_file = os.path.join(MOCK_DATA_DIR, 'mock_chocolate_without_price_01.json')
    #mock_file = os.path.join(MOCK_DATA_DIR, 'mock_udemybeverages_full_01.json')

    with open(mock_file) as json_file:
        data = json.load(json_file)

    return data


def conjoint_q_pairs_one():
    return {
        "cardset": "",
        "maxblocks": 0,
        "maxques": 0,
        "profile_selected": "",
        "max_shown_alternatives": '2',

        "option_none_text": "I would not choose any of these.",
        "has_option_none": "true",

        "ca_config": {
            "Uppers": ["Leather", "Suede", "Imitation leather"],
            "Country": ["Italy", "USA", "Far East"],
            "Price": ["$ 50", "$ 125", "$ 200"],
            "n_alternatives": "2",
            "var_type": [
                # {
                #     "factor": "Uppers",
                #     "type": "cat"
                # },
                # {
                #     "factor": "Country",
                #     "type": "cat"
                # },
                # {
                #     "factor": "Price",
                #     "type": "price"
                # }
            ]
        },

        "design_matrix": "",

        "presented_block": "-1",

        "caonelong_answers": [],
        "caone_analysis_results": [],
        "simulator_data": [],
        "blankitems": [],

        "factors": [
            {
                "label": "Attribute 1",
                "allow_na": "false",
                "type": "cat",
                        "title": "Uppers",
                        "levels": [
                            {"title": "Leather", "label": "Level 1"},
                            {"title": "Suede", "label": "Level 2"},
                            {"title": "Imitation leather", "label": "Level 3"}
                        ]
            },
            {
                "label": "Attribute 2",
                "allow_na": "false",
                "type": "cat",
                        "title": "Country",
                        "levels": [
                            {"title": "Italy", "label": "Level 1"},
                            {"title": "USA", "label": "Level 2"},
                            {"title": "Far East", "label": "Level 3"}
                        ]
            },
            {
                "label": "Attribute 3",
                "allow_na": "false",
                "type": "price",
                        "title": "Price",
                        "levels": [
                            {"title": "$ 50", "label": "Level 1"},
                            {"title": "$ 125", "label": "Level 2"},
                            {"title": "$ 200", "label": "Level 3"}
                        ]
            }
        ],

        "card_profiles": [],
        # "card_profiles": [{'BLOCK': 1, 'QES': 1, 'Uppers_1': 'Suede', 'Country_1': 'Italy', 'Price_1': '$ 200', 'Uppers_2': 'Leather', 'Country_2': 'USA', 'Price_2': '$ 200', 'Uppers_3': 'Leather', 'Country_3': 'Italy', 'Price_3': '$ 50', 'ANSW': ''}, {'BLOCK': 1, 'QES': 2, 'Uppers_1': 'Imitation leather', 'Country_1': 'USA', 'Price_1': '$ 50', 'Uppers_2': 'Suede', 'Country_2': 'Italy', 'Price_2': '$ 200', 'Uppers_3': 'Leather', 'Country_3': 'Far East', 'Price_3': '$ 125', 'ANSW': ''}, {'BLOCK': 1, 'QES': 3, 'Uppers_1': 'Suede', 'Country_1': 'Far East', 'Price_1': '$ 50', 'Uppers_2': 'Leather', 'Country_2': 'Italy', 'Price_2': '$ 50', 'Uppers_3': 'Imitation leather', 'Country_3': 'Italy', 'Price_3': '$ 125', 'ANSW': ''}, {'BLOCK': 2, 'QES': 1, 'Uppers_1': 'Suede', 'Country_1': 'USA', 'Price_1': '$ 125', 'Uppers_2': 'Imitation leather', 'Country_2': 'USA', 'Price_2': '$ 50', 'Uppers_3': 'Suede', 'Country_3': 'Italy', 'Price_3': '$ 200', 'ANSW': ''}, {'BLOCK': 2, 'QES': 2, 'Uppers_1': 'Imitation leather', 'Country_1': 'Far East', 'Price_1': '$ 200', 'Uppers_2': 'Imitation leather', 'Country_2': 'Italy', 'Price_2': '$ 125', 'Uppers_3': 'Imitation leather', 'Country_3': 'USA', 'Price_3': '$ 50', 'ANSW': ''}, {'BLOCK': 2, 'QES': 3, 'Uppers_1': 'Leather', 'Country_1': 'Far East', 'Price_1': '$ 125', 'Uppers_2': 'Imitation leather', 'Country_2': 'Far East', 'Price_2': '$ 200', 'Uppers_3': 'Suede', 'Country_3': 'Far East', 'Price_3': '$ 50', 'ANSW': ''}, {'BLOCK': 3, 'QES': 1, 'Uppers_1': 'Leather', 'Country_1': 'USA', 'Price_1': '$ 200', 'Uppers_2': 'Leather', 'Country_2': 'Far East', 'Price_2': '$ 125', 'Uppers_3': 'Suede', 'Country_3': 'USA', 'Price_3': '$ 125', 'ANSW': ''}, {'BLOCK': 3, 'QES': 2, 'Uppers_1': 'Leather', 'Country_1': 'Italy', 'Price_1': '$ 50', 'Uppers_2': 'Suede', 'Country_2': 'USA', 'Price_2': '$ 125', 'Uppers_3': 'Leather', 'Country_3': 'USA', 'Price_3': '$ 200', 'ANSW': ''}, {'BLOCK': 3, 'QES': 3, 'Uppers_1': 'Imitation leather', 'Country_1': 'Italy', 'Price_1': '$ 125', 'Uppers_2': 'Suede', 'Country_2': 'Far East', 'Price_2': '$ 50', 'Uppers_3': 'Imitation leather', 'Country_3': 'Far East', 'Price_3': '$ 200', 'ANSW': ''}]
    }

# Please indicate if you agree or disagree with the following statements


def matrix_q_default():
    return {
        "question_options": [
            {"id": 1, "subId": 11, "value": "Strongly Disagree",
                "checked": "false", "edit": "false"},
            {"id": 2, "subId": 12, "value": "Disagree",
                "checked": "false", "edit": "false"},
            {"id": 3, "subId": 13, "value": "Neutral",
                "checked": "false", "edit": "false"},
            {"id": 4, "subId": 14, "value": "Agree",
                "checked": "false", "edit": "false"},
            {"id": 5, "subId": 15, "value": "Strongly Agree",
                "checked": "false", "edit": "false"}
        ],
        "variant_options": [
            {"id": 1, "subId": 21, "value": "Product is affordable",
                "checked": "false", "edit": "false"},
            {"id": 2, "subId": 22, "value": "Product does what it claims",
                "checked": "false", "edit": "false"},
            {"id": 3, "subId": 23, "value": "Product is better than other products on the market",
                "checked": "false", "edit": "false"},
            {"id": 4, "subId": 24, "value": "Product is easy to use",
                "checked": "false", "edit": "false"}
        ],
        "selected": [

        ],
        "question_answers": []
    }


def slider_q_default():
    return {
        "scale": {"label": "Hedonic Scale", "val": 2, "color": "red", "track_color": "teal lighten-3"},
        "selected": 5,
        "min": 1,
        "max": 9,
        "ticksLabels": [
            'Dislike extremely',
            '',
            '',
            '',
            'Neither like nor dislike',
            '',
            '',
            '',
            'Dislike extremely'
        ],
        "question_answers": [],
        "summary_answers": []
    }


def ui_data_content_default():
    return {'type': 'defaultType', 'content': 'defaultContent'}


class Survey(models.Model):
    """Survey General"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surveys'
    )

    respondent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='respondents',
        null=True, blank=True
    )

    survey_access_token = models.CharField(
        max_length=255,
        default='lorem',
        null=True, blank=True
    )

    EMAIL = 'EMAIL'
    TOKEN = 'TOKEN'
    PUBLICTOKEN = 'PUBLICTOKEN'
    PUBLIC = 'PUBLIC'
    LOGIN_TYPE = [
        (EMAIL, 'email'),
        (TOKEN, 'token'),
        (PUBLICTOKEN, 'public token'),
        (PUBLIC, 'PUBLIC'),
        #(TEMPORARY, 'temporary'),
    ]
    survey_login_type = models.CharField(
        max_length=255,
        choices=LOGIN_TYPE,
        default=TOKEN,
    )

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    """Completed HTML"""
    completed_html = models.CharField(
        max_length=1500, default="Your survey has been submitted. Thank you!")
    """Welcome HTML"""
    welcome_html = models.CharField(
        max_length=1500, default="Thank you for joining our research initiative!")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    max_nrof_questions = models.IntegerField(
        default=30,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    parentsurvey = models.ForeignKey("self", on_delete=models.CASCADE,
                                     null=True, blank=True)

    objects = SurveyManager()

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    survey_uses_left = models.PositiveIntegerField(
        default=35,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    invitation_sent = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    validity_period_days = models.IntegerField(default=7)

    _clone_model_fields = ['question']

    NOT_PUBLISHED = 'NOT_PUBLISHED'
    PUBLISHED = 'PUBLISHED'
    COMPLETE = 'COMPLETE'
    SURVEY_STATUS = [
        (NOT_PUBLISHED, 'Not Published'),
        (PUBLISHED, 'Published'),
        (COMPLETE, 'Complete'),
    ]
    survey_status = models.CharField(
        max_length=20,
        choices=SURVEY_STATUS,
        default=NOT_PUBLISHED,
        null=True, blank=True,
    )
    SURVEY = 'SURVEY'
    SURVEY_TEMPLATE = 'SURVEY_TEMPLATE'
    SURVEY_TYPE = [
        (SURVEY, 'survey'),
        (SURVEY_TEMPLATE, 'survey_template'),
    ]
    survey_type = models.CharField(
        max_length=255,
        choices=SURVEY_TYPE,
        default=SURVEY,
    )

    EDIT = 'EDIT'
    DISPLAY = 'DISPLAY'
    SURVEY_MODE = [
        (EDIT, 'Edit'),
        (DISPLAY, 'Display'),
    ]
    survey_mode = models.CharField(
        max_length=20,
        choices=SURVEY_MODE,
        default=DISPLAY,
        null=True, blank=True,
    )
    # Cookie name (to disable run survey two times locally)
    cookie_name = models.CharField(max_length=255, null=True, blank=True)
    show_titles = models.BooleanField(default=True, null=True, blank=True)
    show_pages = models.BooleanField(default=True, null=True, blank=True)

    """Navigation"""

    BOTTOM = 'BOTTOM'
    TOP = 'TOP'
    NAVIGATION_BUTTONS = [
        (BOTTOM, 'Bottom'),
        (TOP, 'Top'),
    ]
    show_navigation_buttons = models.CharField(
        max_length=20,
        choices=NAVIGATION_BUTTONS,
        default=BOTTOM,
        null=True, blank=True,
    )
    show_progress_bar = models.BooleanField(default=False)

    """Timer - Quiz"""

    time_to_finish = models.IntegerField(null=True, blank=True)
    time_to_finish_page = models.IntegerField(null=True, blank=True)
    show_timer = models.BooleanField(default=False, null=True, blank=True)
    ALL = 'ALL'
    PAGE = 'PAGE'
    SURVEY = 'SURVEY'
    TIMER_MODE = [
        (ALL, 'All'),
        (PAGE, 'Page'),
        (SURVEY, 'Survey'),
    ]
    show_timer_mode = models.CharField(
        max_length=20,
        choices=TIMER_MODE,
        default=ALL,
        null=True, blank=True,
    )

    survey_properties = models.JSONField(default=default_properties)

    @property
    def isin_validity_period(self):
        if datetime.datetime.now() <= self.start_time + datetime.timedelta(hours=self.validy_period_days):
            return True
        return False

    class Meta:
        unique_together = ['user', 'id']
        verbose_name_plural = "surveys"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        nrof_surveys = Survey.objects.filter(
            parentsurvey=None, user=self.user).count()
        if nrof_surveys >= self.user.max_nrof_surveys:
            raise ValidationError(
                "Your user plan does not support more than {} surveys"
                .format(self.user.max_nrof_surveys)
            )
        super(Survey, self).save(*args, **kwargs)

    def duplicate(self, *args, **kwargs):
        try:
            duplicate_survey = self
            survey_questions = Question.objects.filter(survey__pk=self.id)

            duplicate_survey.parentsurvey_id = self.id
            duplicate_survey.pk = None
            duplicate_survey.uuid = uuid.uuid4()
            duplicate_survey.save()

            for question in survey_questions:
                try:
                    duplicate_question = question
                    duplicate_question.parentquestion_id = question.id
                    duplicate_question.pk = None
                    duplicate_question.uuid = uuid.uuid4()
                    duplicate_question.survey = self
                    duplicate_question.save()
                except ValueError as err:
                    print(err.args)

        except ValueError as err:
            print(err.args)

        return duplicate_survey

    def publish_public(self, *args, **kwargs):
        parent_survey = self
        if parent_survey.survey_status == 'NOT_PUBLISHED':
            parent_survey.survey_status = 'PUBLISHED'
        else:
            print('This survey is already published, SID:', parent_survey.id)
        parent_survey.survey_login_type = 'PUBLIC'
        parent_survey.survey_access_token = 'public' + \
            str(uuid.uuid4().hex)[0:8]

        parent_survey.save()
        return parent_survey

    def make_public_copy(self, *args, **kwargs):

        parent_survey = self
        public_survey = None
        if parent_survey.survey_status == 'PUBLISHED' and   \
                parent_survey.survey_login_type == 'PUBLIC' and \
                parent_survey.survey_uses_left > 0:

            parent_survey.survey_uses_left -= 1
            parent_survey.save()

            public_survey = parent_survey.duplicate()

        return public_survey


class Question(models.Model):
    """Question General"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # assign the manager class to the objects property
    objects = QuestionManager()

    title = models.CharField(max_length=255, default='The question title...')
    description = models.CharField(
        max_length=1500,
        default='The question description...'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    survey = models.ForeignKey(
        Survey,
        related_name='questions',
        on_delete=models.CASCADE
    )

    parentquestion = models.ForeignKey("self", on_delete=models.SET_NULL,
                                       null=True, blank=True)

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    ui_data_content = models.TextField(
        default=ui_data_content_default,
        null=True, blank=True
    )

    EDIT = 'EDIT'
    DISPLAY = 'DISPLAY'
    QUESTION_MODE = [
        (EDIT, 'Edit'),
        (DISPLAY, 'Display'),
    ]
    question_mode = models.CharField(
        max_length=20,
        choices=QUESTION_MODE,
        default=DISPLAY,
        null=True, blank=True,
    )

    NOMINAL = 'NOMINAL'
    ORDINAL = 'ORDINAL'
    SCALE = 'SCALE'
    QUESTION_MEASURE = [
        (NOMINAL, 'Nominal'),
        (ORDINAL, 'Ordinal'),
        (SCALE, 'Scale'),
    ]
    question_measure = models.CharField(
        max_length=20,
        choices=QUESTION_MEASURE,
        default=NOMINAL,
        null=True, blank=True,
    )

    DEFAULTQ = 'DEFAULTQ'
    TEMPLATEQ = 'TEMPLATEQ'
    CHECKBOX = 'CHECKBOX'
    TEXT = 'TEXT'
    RATING = 'RATING'
    SELECTQ = 'SELECTQ'
    DROPDOWN = 'DROPDOWN'
    EMOTION = 'EMOTION'
    RATECUSTOM = 'RATECUSTOM'
    MATRIX = 'MATRIX'
    RATEIMAGE = 'RATEIMAGE'
    SLIDER = 'SLIDER'
    SLIDERCIRCLE = 'SLIDERCIRCLE'
    SLIDERTHREECIRCLE = 'SLIDERTHREECIRCLE'
    SLIDERRANGE = 'SLIDERRANGE'
    UPLOADER = 'UPLOADER'
    SORTABLELIST = 'SORTABLELIST'
    TWOSORTABLELISTS = 'TWOSORTABLELISTS'
    CAPAIRONE = 'CAPAIRONE'

    QUESTION_TYPE = [
        (DEFAULTQ, 'DEFAULT QUESTION'),
        (TEMPLATEQ, 'TEMPLATE QUESTION'),
        (CHECKBOX, 'CHECKBOX'),
        (TEXT, 'TEXT'),
        (RATING, 'RATING'),
        (SELECTQ, 'SELECTQ'),
        (DROPDOWN, 'DROPDOWN'),
        (EMOTION, 'EMOTION'),
        (RATECUSTOM, 'RATE CUSTOM'),
        (MATRIX, 'MATRIX'),
        (RATEIMAGE, 'RATE IMAGE'),
        (SLIDER, 'SLIDER'),
        (SLIDERCIRCLE, 'SLIDER CIRCLE'),
        (SLIDERTHREECIRCLE, 'SLIDER THREE CIRCLE'),
        (SLIDERRANGE, 'SLIDER RANGE'),
        (UPLOADER, 'UPLOADER'),
        (SORTABLELIST, 'SORTABLE LIST'),
        (TWOSORTABLELISTS, 'TWO SORTABLE LISTS'),
        (CAPAIRONE, 'CA PAIR ONE'),
    ]
    question_type = models.CharField(
        max_length=255,
        choices=QUESTION_TYPE,
        default=DEFAULTQ,
    )

    question_properties = models.JSONField(default=default_properties)

    class Meta:
        unique_together = ['user', 'uuid']
        verbose_name_plural = "questions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        nrof_questions = Question.objects.filter(survey=self.survey).count()
        if nrof_questions >= self.survey.max_nrof_questions:
            raise ValidationError(
                "Your survey does not support more than {} questions"
                .format(self.survey.max_nrof_questions)
            )

        if not self.id and self.parentquestion is None and self.question_type == 'CHECKBOX':
            self.question_properties = checkbox_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'EMOTION':
            self.question_properties = emotion_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'RATEIMAGE':
            self.question_properties = rateimage_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'SELECTQ':
            self.question_properties = select_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'MATRIX':
            self.question_properties = matrix_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'SLIDER':
            self.question_properties = slider_q_default()
        if not self.id and self.parentquestion is None and self.question_type == 'CAPAIRONE':
            self.description = 'If these were only options available, which would you choose?'
            self.question_properties = conjoint_q_pairs_one()

            if DATA_DEBUG_MODE == True:
                self.question_properties = mocktest_conjoint_q_pairs_one()

        # BLOCK is presented based on each question per questionnaire generation
        if not self.id and self.parentquestion and self.question_type == 'CAPAIRONE':
            nrof_ca_questions = Question.objects.filter(
                parentquestion=self.parentquestion).count()
            ls = self.question_properties['card_profiles']
            max_blocks = max([el['BLOCK'] for el in ls])
            shown_block = (nrof_ca_questions - 1) % max_blocks + 1
            self.question_properties['presented_block'] = shown_block

        super(Question, self).save(*args, **kwargs)

    def duplicate(self, *args, **kwargs):
        try:
            duplicate_question = self
            duplicate_question.parentquestion_id = self.id
            duplicate_question.pk = None
            duplicate_question.uuid = uuid.uuid4()
            duplicate_question.save()
            duplicate_question.question_properties = self.question_properties
            duplicate_question.save(update_fields=['question_properties'])

        except ValueError as err:
            print(err.args)

        return duplicate_question

    # Slider Question Responses
    def get_slider_analysis_results(self, *args, **kwargs):
        pass

    def get_slider_answers(self, *args, **kwargs):  # Slider Question Responses

        questionanswered = self
        slider_questions = Question.objects.filter(parentquestion=self.id,
                                                   question_type='SLIDER') \
            .values('id', 'question_properties')
        df = read_frame(slider_questions)

        df['selected'] = df['question_properties'].map(lambda x: x['selected'])
        df['min'] = df['question_properties'].map(lambda x: x['min'])
        df['max'] = df['question_properties'].map(lambda x: x['max'])
        df['labels'] = df['question_properties'].map(
            lambda x: x['ticksLabels'])

        if df.empty:
            return questionanswered  # Return Slider Question WITHOUT Responses

        resp1 = df[['id', 'selected', 'min', 'max', 'labels']]

        resp2 = resp1[['selected']].describe().transpose()

        resp1 = resp1.to_json(orient='records')
        resp2 = resp2.to_json(orient='records')
        print(resp1)
        print(resp2)

        questionanswered.question_properties['question_answers'] = resp1
        questionanswered.question_properties['summary_answers'] = resp2
        questionanswered.save()

        return questionanswered  # Return CA One Responses

    def get_caone_long_answers(self, *args, **kwargs):  # CA One Responses

        questionanswered = self
        caone_questions = Question.objects.filter(parentquestion=self.id,
                                                  question_type='CAPAIRONE')\
            .annotate(
            questionproperties=F('question_properties'),
            userid=F('user'),
            sid=F('survey'))\
            .values('id', 'sid', 'userid', 'questionproperties')

        df = read_frame(caone_questions)

        if df.empty:
            return questionanswered  # Return CA One WITHOUT Responses

        number_of_questions = df.shape[0]
        appended_data = []
        for i in range(number_of_questions):

            presented_block = df['questionproperties'][i]['presented_block']
            alternatives_nr = max(
                [el['ALT'] for el in df['questionproperties'][i]['design_matrix']])

            answ_df1 = df['questionproperties'][i]['card_profiles']
            answ_df2 = pd.DataFrame(answ_df1)
            answ_df2 = answ_df2.loc[answ_df2['BLOCK'] == presented_block]
            answ_df3 = answ_df2.fillna({'ANSW': ''}, inplace=False)
            answ_df3['RES'] = answ_df3['ANSW'].replace('', alternatives_nr - 1)

            gen = ['BLOCK', 'QES', 'ANSW', 'RES']
            allfact = [colnam for colnam in list(
                answ_df3.columns) if colnam not in gen]

            stb_cols = f7([el.split("_")[0]
                           for el in allfact])  # UNIQUE PRESERVE ORDER!!

            answ_df3['QESBLOCK'] = answ_df3.index
            answ_df4 = pd.wide_to_long(
                answ_df3, stubnames=stb_cols, i="QESBLOCK", j="ALT", sep='_')

            answ_df4.reset_index(inplace=True)

            answ_df4['CHOICE'] = (answ_df4['ALT'] == (answ_df4['RES'] + 1))
            answ_df5 = answ_df4.sort_values(by=['BLOCK', 'QES', 'ALT'])
            answ_df6 = answ_df5.reset_index(drop=True)
            answ_df6 = answ_df6.drop(['QES'], axis=1)
            answ_df6['RES'] = df['id'][i]
            answ_df6['STR'] = answ_df6['RES'].astype(
                str) + '0' + answ_df6['QESBLOCK'].astype(str)

            appended_data.append(answ_df6)

        resp1 = pd.concat(appended_data, ignore_index=True)
        resp1 = resp1.to_json(orient='records')

        questionanswered.question_properties['caonelong_answers'] = resp1
        questionanswered.save()

        return questionanswered  # Return CA One Responses

    # CA One Analysis Results -- DB Call Approach

    def get_caone_analysis_results(self, *args, **kwargs):

        questionanswered = self
        caone_long_answers = questionanswered.question_properties['caonelong_answers']
        if caone_long_answers == []:  # If no answers then return the same question..
            return questionanswered

        print("~~~~ANALYSIS RESULTS~~~~~~", datetime.now())
        try:
            response = requests.post(
                "http://localhost:8001/get_caone_results", headers={"Content-Type": "application/json"}, data=json.dumps({
                    "question_id": questionanswered.id
                })
            )
            response_json = response.json()

            if isinstance(response_json, dict) == False:
                print('hopa----->> ', type(response_json))
                raise ValidationError(response_json)

            questionanswered.question_properties['caone_analysis_results'] = response_json['pw']
            questionanswered.question_properties['simulator_data'] = response_json['simmatrix']
            all_factors = questionanswered.question_properties['factors']
            factors = [f['title'] for f in all_factors]
            questionanswered.question_properties['blankitems'] = 5 * [
                {fttl: "" for fttl in factors}]
            questionanswered.save()

            print(response_json)

            if isinstance(response_json, dict) == False:
                raise ValidationError(response_json)

        except ConnectionError:
            raise ValidationError(
                {'R_SERVICE': 'R Server is not reachable (connection error)!'})

        return questionanswered


def upload_participants(instance, filename):
    return "surveys/takensurvey_{survey_uuid}_{uploader_name}/{filename}".format(
        uploader_name=instance.user.username,
        survey_uuid=instance.survey.uuid,
        filename=filename
    )


class ParticipantsDocument(models.Model):

    """
    Participants list is a .csv or .txt file uploaded and contains columns
    EMAIL, FIRSTNAME, LASTNAME, TOKEN, COMMENTS
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        Survey,
        related_name='participants_document',
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(
        upload_to=upload_participants,
        blank=True, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    filter_blank_email_addresses = models.BooleanField(default=True)
    allow_invalid_email_addresses = models.BooleanField(default=False)
    filter_duplicate_records = models.BooleanField(default=True)

    duplicates_determined_by = models.JSONField(
        default=default_duplicatescheck
    )
    typed_participantslist = models.JSONField(default=dict)

    SEMICOLON = 'SEMICOLON'
    COMMA = 'COMMA'
    TAB = 'TAB'
    SEPARATOR_USED = [
        (SEMICOLON, 'SEMICOLON'),
        (COMMA, 'COMMA'),
        (TAB, 'TAB'),
    ]
    separator_used = models.CharField(
        max_length=20,
        choices=SEPARATOR_USED,
        default=COMMA,
        null=True, blank=True,
    )

    @property
    def uploadedfile_separator(self):
        separator = ''
        if self.separator_used == 'COMMA':
            separator = ','
        if self.separator_used == 'SEMICOLON':
            separator = ';'
        if self.separator_used == 'TAB':
            separator = '\\t'
        return separator

    def assign_respondent(self, df, parent_survey_id):

        new_respondents = 0
        for index, row in df.iterrows():

            answer_token_uuid = uuid.uuid4().hex
            answer_token = str(answer_token_uuid)[0:5]
            rev_answer_token = str(answer_token_uuid)[-5:]

            respondents_emails = User.objects.filter(
                email=row['EMAIL']).values_list('email', flat=True)
            user = None
            respondent = None
            if row['EMAIL'] in respondents_emails:
                """
                When the user email already exist
                """
                respondent = User.objects.get(email=row['EMAIL'])
            else:
                """
                When the user email is New
                """
                user = User.objects.create(
                    username=row['EMAIL'].split('@')[0] + rev_answer_token,
                    #username = answer_token,
                    email=row['EMAIL'],
                    first_name=row['FIRSTNAME'],
                    last_name=row['LASTNAME'],
                )
                user.set_password(answer_token)
                user.save()
                respondent = user

            print('~~~~~~~~~~~~~~~', respondent)

            all_parent_survey_respondents = Survey.objects.filter(
                parentsurvey=parent_survey_id
            ).values_list('respondent', flat=True)
            if respondent in all_parent_survey_respondents:
                print('---IS ALREADY RESPONDENT---', respondent)
                continue
            print('~~~~~~~~~~~~~~~', respondent)

            parent_survey = Survey.objects.get(pk=parent_survey_id)
            new_survey = parent_survey.duplicate()
            new_survey.respondent = respondent
            new_survey.survey_access_token = answer_token
            new_survey.save()

            new_respondents += 1

        return '%s respondents were uploaded and %s were assigned to new surveys' % (df.shape[0], new_respondents)

    def save(self, *args, **kwargs):

        if self.document:
            try:
                df = self.document.read().decode('utf-8')
                df1, invalid_emails, no_valid_records = clean_input_list(
                    df, self.duplicates_determined_by)

                # Create respondents
                new_respondents = self.assign_respondent(df1, self.survey.id)
                print('------------------', new_respondents)

            except pd.errors.EmptyDataError:
                print('Note: filename.csv was empty. Skipping.')
                pass  # will skip the rest of the block and move to next file

        if self.typed_participantslist:
            df = self.typed_participantslist
            df1, invalid_emails, no_valid_records = clean_input_list(
                df, self.duplicates_determined_by)

            # Create respondents
            new_respondents = self.assign_respondent(df1, self.survey.id)
            print('------------------', new_respondents)

        super(ParticipantsDocument, self).save(*args, **kwargs)
