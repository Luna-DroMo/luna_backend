from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import StudentUser


@receiver(post_save, sender=StudentUser)
def create_student_forms(sender, instance, created, **kwargs):

    if created:
        from core.models import Form, StudentForm
        student = instance
        forms = Form.objects.all()
        for form in forms:
            StudentForm.objects.create(
                student=student, form_id=form.pk, resolution="NOT_COMPLETED")
