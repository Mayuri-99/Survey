from email.message import EmailMessage
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .forms import AnswerForm, QuestionForm
from .models import Question, Answer
from django.core.cache import cache
from django.views import View  # Import View class

from .forms import forms
from .tokens import generate_token # type: ignore

from mysite import settings
from django.core.mail import send_mail
# Clear all keys in the cache
cache.clear()
# Create your views here.
@csrf_protect
def home(request):
    return render(request,"home.html")

def signin(request):
    if request.method =="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
    else:
        return render(request, "login.html")
    
def signout(request):
    logout(request)
    return render(request, "login.html")
def signup(request):
    if request.method =="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confpassword=request.POST.get('confpassword')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if password != confpassword :
            messages.error(request, "Password didn't match !")
            messages.success(request ,"Your account has been successfully created.")

        if password == confpassword:
            # Create and save the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.name = username
            user.is_active=False
            # Alternatively, you can set the password after creating the user
            # user = User.objects.create_user(username=username, email=email)
            # user.set_password(password)
            user.save()
            # Log the user in
            messages.success(request, "Your account has been successfully created")
            #Email
            subject ="Welcome to survey login!"
            message = "Hello " + user.name +" !!\n" "Welcome to survey !!\n Thank you for visiting \n we have also sent you confirmation email , please confirm email address in order to activate your account."
            from_email= settings.EMAIL_hOST_USER
            to_list =[user.email]
            send_mail(subject, from_email, message,to_list,fail_silently=True )

            #Email address confirmation mail
            get_current_site = get_current_site(request,) 
            email_subject = "Confirm your email @mysite-survey login"
            message2 = render_to_string('email_confirmation.html',{
                'name':user.name,
                'domain': current_site_domain,  # type: ignore
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),

            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            login(request, user)
            return redirect('/signin')
        else:
            return redirect('/signup')
    else:
        return render(request, 'signup.html')
    
def forgotpwd(request):
        return render(request,"forgotpwd.html")
def activate(request, uidb64, token):
    try:
        uid= force_text(urlsafe_base64_decode(uidb64)) # type: ignore
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExistoesnot):
        user=None
    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
def survey_form(request):
        return render(request,"survey_form.html")

class SurveyView(View):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'survey.html', {'form': form})
    
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('add_answers', question_id=question.id)
        return render(request, 'survey.html', {'form': form})

class AddAnswersView(View):
    def get(self, request, question_id):
        question = Question.objects.get(id=question_id)
        return render(request, 'add_answers.html', {'question': question})
    
    def post(self, request, question_id):
        question = Question.objects.get(id=question_id)
        answer_text = request.POST.get('answer_text')
        Answer.objects.create(question=question, answer_text=answer_text)
        return redirect('survey')
  
  
def new_question(request):
    return render(request, 'new_question.html')

def edit_submitted_data(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=0)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)
    
    if request.method == 'POST':
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.all())
        answer_formset = AnswerFormSet(request.POST, queryset=Answer.objects.all())
        
        if question_formset.is_valid() and answer_formset.is_valid():
            question_formset.save()
            answer_formset.save()
            return redirect('submitted_data')
    else:
        question_formset = QuestionFormSet(queryset=Question.objects.all())
        answer_formset = AnswerFormSet(queryset=Answer.objects.all())
    
    context = {
        'question_formset': question_formset,
        'answer_formset': answer_formset,
    }
    return render(request, 'edit_submitted_data.html', context)