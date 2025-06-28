from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import SupportTicket, SupportMessage
from .forms import SupportTicketForm, SupportMessageForm

@login_required
def ticket_list(request):
    if getattr(request.user, "role", None) in ("admin", "tutor", "guide") or request.user.is_superuser:
        tickets = SupportTicket.objects.all().order_by('-created_at')
    else:
        tickets = SupportTicket.objects.filter(created_by=request.user)
    return render(request, "support/ticket_list.html", {"tickets": tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    messages = ticket.messages.order_by('created_at')
    message_form = SupportMessageForm()
    if request.method == "POST":
        message_form = SupportMessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            msg = message_form.save(commit=False)
            msg.ticket = ticket
            msg.user = request.user
            msg.save()
            return redirect("support_ticket_detail", pk=ticket.pk)
    return render(request, "support/ticket_detail.html", {"ticket": ticket, "messages": messages, "message_form": message_form})

@login_required
def ticket_create(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect("support_ticket_detail", pk=ticket.pk)
    else:
        form = SupportTicketForm()
    return render(request, "support/ticket_form.html", {"form": form})

@user_passes_test(lambda u: u.is_superuser or getattr(u, "role", None) in ("admin", "tutor", "guide"))
def ticket_assign(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == "POST":
        ticket.assigned_to_id = request.POST.get("assigned_to")
        ticket.save()
        return redirect("support_ticket_detail", pk=pk)
    return render(request, "support/ticket_assign.html", {"ticket": ticket})

@user_passes_test(lambda u: u.is_superuser or getattr(u, "role", None) in ("admin", "tutor", "guide"))
def ticket_resolve(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == "POST":
        ticket.status = "resolved"
        ticket.resolution = request.POST.get("resolution")
        ticket.save()
        return redirect("support_ticket_detail", pk=pk)
    return render(request, "support/ticket_resolve.html", {"ticket": ticket})