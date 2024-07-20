from django.shortcuts import render, get_object_or_404, redirect
from . import models

import markdown

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SemesterForm, AssignmentAnswerForm, MaterialForm, AssignmentForm, MarksForm

# Create your views here.

def total_unsubmitted_assignments_for_user_in_semester(user, semester):
    # Get all assignment IDs for the semester
    all_assignments_ids = models.Assignment.objects.filter(chapter__subject__semester=semester).values_list('id', flat=True)
    
    # Get all submitted assignment IDs for the user
    submitted_assignments_ids = models.AssignmentAnswer.objects.filter(user=user, assignment__in=all_assignments_ids).values_list('assignment_id', flat=True)
    
    # Count the unsubmitted assignments
    unsubmitted_assignments_count = models.Assignment.objects.filter(id__in=all_assignments_ids).exclude(id__in=submitted_assignments_ids).count()
    return unsubmitted_assignments_count

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if (request.method == "POST"):
        form = SemesterForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('index')
    else:
        form = SemesterForm()

    current_user = request.user

    try:
        role = models.UserRole.objects.get(user=current_user)
    except:
        role = None

    
    subjects = models.Subject.objects.filter(semester=current_user.userrole.semester)
    sgpas_instance = models.Sgpa.objects.filter(user=current_user)
    sgpas = [gpa.gpa for gpa in sgpas_instance]

    sgpas = sgpas + [0] * (8 - len(sgpas))
    count = 0
    cgpa = 0.0
    for sgpa in sgpas:
        if sgpa != 0.0:
            cgpa += sgpa
            count += 1
    
    if count != 0:
        cgpa /= count
    else:
        cgpa = 0

    total_assignments = models.Assignment.objects.filter(chapter__subject__semester=current_user.userrole.semester).count()
    unsubmitted_assignments = total_unsubmitted_assignments_for_user_in_semester(current_user, current_user.userrole.semester)

    submitted_assignments = total_assignments - unsubmitted_assignments
    
    context = {
        'subjects': subjects,
        'sgpas': sgpas,
        'cgpa': cgpa,
        'role': role,
        'form': form,
        'total_assignments': submitted_assignments,
        'unsubmitted_assignments': unsubmitted_assignments,
    }

    return render(request, 'index.html', context)


def semester_details(request, slug):

    if not request.user.is_authenticated:
        return redirect('login')

    semester = models.Semester.objects.get(slug=slug)
    subjects = models.Subject.objects.filter(semester=semester)

    context = {
        'semester': semester,
        'subjects': subjects
    }

    return render(request, 'semester_details.html', context)


def subject_details(request, slug):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    subject = models.Subject.objects.get(slug=slug)
    chapters = models.Chapter.objects.filter(subject=subject)
    try:
        syllabus_instance = models.Syllabus.objects.get(subject=subject)
        if syllabus_instance.content:
            syllabus = markdown.markdown(syllabus_instance.content)
        else:
            syllabus = ""
    except:
        syllabus_instance = None
        syllabus = ""

    

    context = {
        'subject': subject,
        'chapters': chapters,
        'syllabus': syllabus
    }

    return render(request, 'subject_details.html', context)


def chapter_details(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    chapter = models.Chapter.objects.get(slug=slug)
    materials = models.Material.objects.filter(chapter=chapter)
    assignments = models.Assignment.objects.filter(chapter=chapter)

    if request.method == 'POST':
        if 'material_submit' in request.POST:
            material_form = MaterialForm(request.POST, request.FILES)
            if material_form.is_valid():
                saved_material_form = material_form.save(commit=False)
                saved_material_form.chapter = chapter
                saved_material_form.save()
                return redirect('chapter_details', chapter.slug)
        elif 'assignment_submit' in request.POST:
            assignment_form = AssignmentForm(request.POST)
            if assignment_form.is_valid():
                # Handle the assignment form saving process here
                saved_assignment_form = assignment_form.save(commit=False)
                saved_assignment_form.chapter = chapter
                saved_assignment_form.save()
                return redirect('chapter_details', chapter.slug)
    else:
        material_form = MaterialForm()
        assignment_form = AssignmentForm()

    context = {
        'chapter': chapter,
        'materials': materials,
        'assignments': assignments,
        'material_form': material_form,
        'assignment_form': assignment_form,
    }

    return render(request, 'chapter_details.html', context)


def assignment_details(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    
    assignment = models.Assignment.objects.get(slug=slug)
    submitted = models.AssignmentAnswer.objects.filter(assignment=assignment, user=request.user).exists()

    if request.method == "POST":
        form = AssignmentAnswerForm(request.POST, request.FILES)

        if form.is_valid():
            assignment_answer = form.save(commit=False)
            assignment_answer.assignment = assignment
            assignment_answer.user = request.user
            assignment_answer.marks = 0
            assignment_answer.date = timezone.now()
            assignment_answer.save()
            return redirect('assignment_details', assignment.slug)

    else:
        form = AssignmentAnswerForm()

    

    context = {
        'assignment': assignment,
        'form': form,
        'submitted': submitted,
    }

    return render(request, 'assignment_details.html', context)

def success(request):
    return render(request, 'success.html')


def all_assignment_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.userrole.role == 'admin' or request.user.userrole.role == 'teacher'):
        return redirect('index')

    assignment = get_object_or_404(models.Assignment, slug=slug)
    all_assignments = models.AssignmentAnswer.objects.filter(assignment=assignment)

    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            assignment_answer_id = request.POST.get('assignment_answer_id')
            assignment_answer = get_object_or_404(models.AssignmentAnswer, id=assignment_answer_id)
            assignment_answer.marks = form.cleaned_data['marks']
            assignment_answer.save()
            return redirect('all_assignments', slug=slug)
    else:
        form = MarksForm()

    context = {
        'assignment': assignment,
        'all_assignments': all_assignments,
        'form': form,
    }

    return render(request, 'all_assignments.html', context)

def user_assignments(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    assignments = models.AssignmentAnswer.objects.filter(user=user)

    context = {
        'assignments': assignments,
    }

    return render(request, 'user_assignments.html', context)