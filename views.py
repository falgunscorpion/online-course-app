from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Submission, Question, Choice

def submit(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    if request.method == 'POST':
        selected_choices = request.POST.getlist('choice')

        submission = Submission.objects.create(enrollment=enrollment)

        for choice_id in selected_choices:
            choice = Choice.objects.get(id=int(choice_id))
            submission.choices.add(choice)

        return show_exam_result(request, course_id)


def show_exam_result(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.filter(enrollment=enrollment).last()

    total_score = 0
    possible_score = 0

    for question in Question.objects.filter(lesson__course=course):
        possible_score += 1

        correct_choices = question.choice_set.filter(is_correct=True)
        selected_choices = submission.choices.filter(question=question)

        if set(correct_choices) == set(selected_choices):
            total_score += 1

    context = {
        'course': course,
        'total_score': total_score,
        'possible_score': possible_score,
    }

    return render(request, 'exam_result.html', context)
