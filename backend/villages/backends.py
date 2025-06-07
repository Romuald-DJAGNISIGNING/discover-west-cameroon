
# Custom backends or utilities for the villages app can be placed here.

# Example: Custom methods to fetch village details or tourist information
def get_village_details(village_id):
    try:
        village = Village.objects.get(id=village_id)
        attractions = Attraction.objects.filter(village=village)
        local_sites = LocalSite.objects.filter(village=village)
        return {
            'village': village,
            'attractions': attractions,
            'local_sites': local_sites
        }
    except Village.DoesNotExist:
        return None
