from import_export import resources
from .models import movieinfo

class MovieInfoResource(resources.ModelResource):
    class Meta:
        model =movieinfo
