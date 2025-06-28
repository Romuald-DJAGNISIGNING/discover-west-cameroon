from django.shortcuts import render, get_object_or_404
from .models import Village

def village_map_view(request, pk):
    village = get_object_or_404(Village, pk=pk)
    return render(request, "village_map.html", {"village": village})