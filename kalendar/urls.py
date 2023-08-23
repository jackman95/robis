from django.urls import path
from kalendar.views import(
    create_kalendar_view,
    event_detail_view,
    event_edit_view,
    event_entry_view,
    event_participans_download_csv,
    event_participans_download_xlsx,
    event_entry_edit_view,
    event_entry_edit_all_view,
)


app_name = 'kalendar'

urlpatterns = [
    path('vytvorit/', create_kalendar_view, name="create"),
    path('<slug:slug>/', event_detail_view, name="event"),
    path('<slug>/uprava/', event_edit_view, name="edit"),
    path('<slug>/prihlaska/', event_entry_view, name="entry"),
    path('<slug:slug>/ucastnici_csv/', event_participans_download_csv, name='download_participants_csv'),
    path('<slug:slug>/ucastnici_xlsx/', event_participans_download_xlsx, name='download_participants_xlsx'),
    path('<slug:slug>/prihlaska_uprava/', event_entry_edit_view, name='entry_edit'),
    path('<slug:slug>/prihlasky_uprava/', event_entry_edit_all_view, name='entry_edit_all'),


    ]