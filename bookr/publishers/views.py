from django.shortcuts import render, redirect, get_object_or_404
from reviews.models import Publisher
from .forms import PublisherForm
from django.contrib import messages

def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f'Publisher {updated_publisher} was successfully created')
            else:
                messages.success(request, f'Publisher {updated_publisher} was successfully updated')
            return redirect('publisher_edit', updated_publisher.pk)

    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'publishers/publishers.html', {'form':form})

