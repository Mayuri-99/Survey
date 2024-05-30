from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'answer_type']
 
 

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']