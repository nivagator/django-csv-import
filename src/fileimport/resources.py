from import_export import resources
from .models import Warehouse

class WarehouseResource(resources.ModelResource):
    class Meta:
        model = Warehouse