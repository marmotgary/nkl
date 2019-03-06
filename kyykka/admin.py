from django.contrib import admin
from kyykka.models import Team, Season, PlayersInTeam, Match, Throw

# Register your models here.

class PlayersInTeamInline(admin.TabularInline):
    '''
    This is required to display PlayersInTeam at the admin panel,
    because the "through" attribute is used with the Team players ManyToManyField
    '''
    model = PlayersInTeam
    extra = 1

class PlayersInTeamAdmin(admin.ModelAdmin):
    inlines = (PlayersInTeamInline,)

admin.site.register(Team, PlayersInTeamAdmin)
admin.site.register(Season)
admin.site.register(PlayersInTeam)
admin.site.register(Match)
admin.site.register(Throw)
