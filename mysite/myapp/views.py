from django.shortcuts import render , redirect
from .models import Task
from .forms import Todoform
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView , DeleteView
from django.urls import reverse_lazy



# class based generic views

# for lisiting out all the objects inside our Model or database
class Tasklistview(ListView):
    model = Task
    template_name = 'myapp/index.html'
    context_object_name = 'task_list'
    #ordering = 'priority'

# class based detail view
class Taskdetailview(DetailView):
    model = Task
    template_name = 'myapp/detail.html'
    context_object_name = 'task'
    
# class based update view for updating
class Taskupdateview(UpdateView):
    model = Task
    template_name = 'myapp/update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    # return back to that modified page
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
    
# class based view for delete object

class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'myapp/delete.html'
    success_url = reverse_lazy('cbvindex')
    
    



# function based views
def index(request):
    if request.method =="POST":
        name = request.POST.get('name','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date','')
        #create object of nodel to save that data into out databse
        task = Task(name=name, priority=priority , date=date)
        task.save()
        return redirect('/')
    
    task_list = Task.objects.all()
    return render(request,'myapp/index.html',{'task_list':task_list})


def delete(request,taskid):
    task = Task.objects.get(id=taskid)
    if request.method=="POST":
        task.delete()
        return redirect('/')
    
    return render(request,'myapp/delete.html',{'task':task})



def update(request,id):
    task =Task.objects.get(id=id)
    form = Todoform(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'myapp/edit.html',{ 'form':form , 'task':task })
    