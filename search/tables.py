import django_tables2 as tables
from search.models import WebSite

class WebSiteTable(tables.Table):
    rank = tables.Column()
    class Meta:
        model = WebSite
        sequence = ("rank", "title", "url", "body", "pub_date", "id")
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
