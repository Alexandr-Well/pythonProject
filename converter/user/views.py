import os
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.uploadedfile import SimpleUploadedFile
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from .forms import RegistrationUserForm, LoginUserForm, FileForm
from .models import File
from django.db import models
from .logic import xlsx_get_file, remove_temp_dir


class RegisterUser(CreateView):
    """ standard user registration form"""
    form_class = RegistrationUserForm
    template_name = "user/add_user.html"
    success_url = reverse_lazy("user_info")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_info')


class LoginUser(LoginView):
    """standard login form"""
    form_class = LoginUserForm
    template_name = "user/user_auth.html"
    success_url = reverse_lazy("user_info")


def logout_user(request):
    """logout form"""
    logout(request)
    return redirect('login')


class GetFile(LoginRequiredMixin, TemplateView):
    """GetFile don't need right now just template to feature"""
    template_name = 'user/get_file.html'
    login_url = 'login'
    redirect_field_name = ''

    def get_context_data(self, **kwargs):
        files = File.objects.filter(user__username=self.request.user.username)
        if len(files) > 5:
            files.first().delete()
        kwargs.update({
            "files": files[::-1][0]
        })
        return super().get_context_data(**kwargs)


class ViewUserInfo(LoginRequiredMixin, FormView):
    """
    main logic
    """
    template_name = 'user/user_info.html'
    login_url = 'login'
    form_class = FileForm

    def get_context_data(self, **kwargs):
        files = File.objects.filter(user__username=self.request.user.username)
        if len(files) > 5:
            files.first().delete()
        kwargs.update({
            "files": files[::-1]
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form, **kwargs):
        try:
            remove_temp_dir(str(self.request.user.username))
        except FileNotFoundError:
            pass
        file = self.request.FILES.get('file')
        file_name = str(self.request.FILES.get('file'))
        compression = self.request.POST.get('value')
        kmz_file = f'{(xlsx_get_file(file, compression, self.request.user.username, file_name))}.kmz'
        file_path = os.path.join("temp", kmz_file)
        kmz_uploader = SimpleUploadedFile(file_path, open(file_path, 'rb').read())
        File.objects.create(file=kmz_uploader, user=self.request.user, title=file_name)
        remove_temp_dir(str(self.request.user.username))
        self.get_context_data(object=self.request)
        return redirect(self.request.path)


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


@receiver(models.signals.post_delete, sender=File)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on post_delete """
    if instance.file:
        _delete_file(instance.file.path)
