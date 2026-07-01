from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.db.models import Q
from .models import students, Attendance
from .forms import studentsForm

def dashboard(request):
    total_students = students.objects.count()
    
    # Calculate unique courses
    total_courses = students.objects.values('course').distinct().count()
    
    # Calculate today's attendance rate
    today = timezone.localdate()
    total_today = Attendance.objects.filter(date=today).count()
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    attendance_rate = round((present_today / total_today) * 100) if total_today > 0 else 0
    
    # Recent registrations (last 5)
    recent_students = students.objects.order_by('-id')[:5]
    
    # Course distribution for dashboard display
    course_list = students.objects.values('course').distinct()
    courses_data = []
    for c in course_list:
        course_name = c['course']
        count = students.objects.filter(course=course_name).count()
        courses_data.append({
            'name': course_name,
            'count': count,
            # calculate percentage of total students in this course
            'pct': round((count / total_students) * 100) if total_students > 0 else 0
        })
    
    context = {
        "total_students": total_students,
        "total_courses": total_courses,
        "attendance_rate": attendance_rate,
        "recent_students": recent_students,
        "courses_data": courses_data,
        "today": today,
    }
    return render(request, "students/dashboard.html", context)

def students_list(request):
    search = request.GET.get('search', '')
    if search:
        all_students = students.objects.filter(
            Q(name__icontains=search) | 
            Q(roll__icontains=search) | 
            Q(email__icontains=search) | 
            Q(course__icontains=search)
        )
    else:
        all_students = students.objects.all()
        
    return render(request, "students/students_list.html", {"students": all_students, "search": search})

def students_add(request):
    if request.method == "POST":
        form = studentsForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student '{student.name}' has been added successfully!")
            return redirect("students_list")
    else:
        form = studentsForm()
        
    return render(request, "students/students_add.html", {"form": form})

def students_edit(request, pk):
    student = get_object_or_404(students, pk=pk)
    if request.method == "POST":
        form = studentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student '{student.name}' has been updated successfully!")
            return redirect("students_list")
    else:
        form = studentsForm(instance=student)
        
    return render(request, "students/students_edit.html", {"form": form, "student": student})

def students_delete(request, pk):
    student = get_object_or_404(students, pk=pk)
    if request.method == "POST":
        name = student.name
        student.delete()
        messages.success(request, f"Student '{name}' has been deleted successfully!")
        return redirect("students_list")
    return render(request, "students/students_confirm_delete.html", {"student": student})

def attendance(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = date.fromisoformat(date_str)
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()
        
    all_students = students.objects.all()
    
    # Save/Update Attendance
    if request.method == "POST":
        for s in all_students:
            status = request.POST.get(f"attendance_{s.id}")
            if status in ['Present', 'Absent']:
                Attendance.objects.update_or_create(
                    student=s,
                    date=selected_date,
                    defaults={'status': status}
                )
        messages.success(request, f"Attendance for {selected_date} has been saved successfully!")
        return redirect(f"/attendance/?date={selected_date.isoformat()}")
        
    existing_attendance = Attendance.objects.filter(date=selected_date)
    attendance_dict = {a.student_id: a.status for a in existing_attendance}
    
    context = {
        "students": all_students,
        "selected_date": selected_date.isoformat(),
        "attendance_dict": attendance_dict,
    }
    return render(request, "students/attendance.html", context)

def attendance_report(request):
    all_students = students.objects.all()
    total_sessions = Attendance.objects.values('date').distinct().count()
    
    report = []
    for s in all_students:
        student_sessions = Attendance.objects.filter(student=s).count()
        present_count = Attendance.objects.filter(student=s, status='Present').count()
        
        if student_sessions > 0:
            rate = round((present_count / student_sessions) * 100)
        else:
            rate = 0
            
        report.append({
            "student": s,
            "total_days": student_sessions,
            "present_days": present_count,
            "absent_days": student_sessions - present_count,
            "rate": rate
        })
        
    # Overall attendance rate for school
    total_records = Attendance.objects.count()
    total_present = Attendance.objects.filter(status='Present').count()
    overall_rate = round((total_present / total_records) * 100) if total_records > 0 else 0
    
    context = {
        "report": report,
        "total_sessions": total_sessions,
        "overall_rate": overall_rate,
    }
    return render(request, "students/attendance_report.html", context)