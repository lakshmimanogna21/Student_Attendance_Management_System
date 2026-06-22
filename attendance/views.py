from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance
from accounts.models import CustomUser
import datetime

@login_required
def student_dashboard(request):
    attendance = Attendance.objects.filter(student=request.user).order_by('-date')
    total = attendance.count()
    present_count = attendance.filter(status='Present').count()
    absent_count = attendance.filter(status='Absent').count()
    return render(request, 'attendance/student_dashboard.html', {
        'attendance': attendance,
        'total': total,
        'present_count': present_count,
        'absent_count': absent_count,
    })

@login_required
def teacher_dashboard(request):
    students = CustomUser.objects.filter(role='student')
    today = datetime.date.today()
    
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status}
                )
        return redirect('teacher_dashboard')
    
    return render(request, 'attendance/teacher_dashboard.html', {
        'students': students,
        'today': today,
    })

@login_required
def admin_dashboard(request):
    students = CustomUser.objects.filter(role='student')
    all_attendance = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/admin_dashboard.html', {
        'students': students,
        'all_attendance': all_attendance,
    })