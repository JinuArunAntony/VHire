from .models import MenuItem

def menu_items(request):
    # Retrieve menu items from the database
    menu_items = MenuItem.objects.all()
    return {'menu_items': menu_items}