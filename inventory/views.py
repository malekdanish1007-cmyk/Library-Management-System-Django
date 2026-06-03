from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Item
from .forms import ItemForm
from users.models import AuditLog

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, "inventory/item_list.html", {"items": items})

@login_required
@user_passes_test(is_admin)
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            AuditLog.objects.create(
                user=request.user,
                action='CREATE',
                description=f'Item "{item.name}" created.',
                ip_address=request.META.get('REMOTE_ADDR'),
            )
            return redirect("item_list")
    else:
        form = ItemForm()
    return render(request, "inventory/item_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                user=request.user,
                action='UPDATE',
                description=f'Item "{item.name}" updated.',
                ip_address=request.META.get('REMOTE_ADDR'),
            )
            return redirect("item_list")
    else:
        form = ItemForm(instance=item)
    return render(request, "inventory/item_form.html", {"form": form, "item": item})

@login_required
@user_passes_test(is_admin)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    AuditLog.objects.create(
        user=request.user,
        action='DELETE',
        description=f'Item "{item.name}" deleted.',
        ip_address=request.META.get('REMOTE_ADDR'),
    )
    item.delete()
    return redirect("item_list")