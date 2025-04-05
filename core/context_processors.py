from .models import SchoolSettings

def school_settings(request):
    """
    Context Processor: Fetches the SchoolSettings object globally for all templates.

    This function is automatically called by Django on every request to provide the school
    settings to all templates via the context.
    
    - The first SchoolSettings object is retrieved to ensure that only one instance of the settings exists.
    - The 'school_settings' variable is returned as a dictionary so it can be accessed in all templates.
    """
    return {
        "school_settings": SchoolSettings.objects.first()  # Retrieves the first (and only) SchoolSettings instance.
    }
