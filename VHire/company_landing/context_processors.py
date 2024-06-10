from company_landing.models import Com_Landing_MenuItem

def com_lan_menu_items(request):
    # Retrieve menu items from the database
    menu_items = Com_Landing_MenuItem.objects.all()
    return {'com_lan_menu_items': menu_items}