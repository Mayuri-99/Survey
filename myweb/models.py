from django.db import models

class Question(models.Model):
    TEXT = 'input'
    TEXTAREA = 'textarea'
    RADIO = 'radio'
    CHECKBOX = 'checkbox'
    RANGE = 'range'
    
    ANSWER_CHOICES = [
        (TEXT, 'Input'), 
        (TEXTAREA, 'Textarea'),
        (RADIO, 'Radio'),
        (CHECKBOX, 'Checkbox'),
        (RANGE, 'Range')
    ]
    
    question_text = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    
    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    
    def __str__(self):
        return f"{self.question}: {self.answer_text}"
    
def submitted_data(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    context = {
        'questions': questions,
        'answers': answers,
    }
    return render(request, 'submitted_data.html', context)