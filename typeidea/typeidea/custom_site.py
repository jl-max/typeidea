from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = "Typeidea"
    site_title = "Typeidea admin"
    index_title = "Index"


custom_site = CustomSite(name="cus_admin")
