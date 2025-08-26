# scraper_app/export.py

import pandas as pd
import json
from .models import Site

def export_data(format_type):
    sites = Site.objects.all()
    data = [{"url": site.url, "title": site.title, "description": site.description, "last_scraped": site.last_scraped} for site in sites]

    if format_type == 'csv':
        df = pd.DataFrame(data)
        df.to_csv('exported_data.csv', index=False)
        return 'exported_data.csv'
    elif format_type == 'json':
        with open('exported_data.json', 'w') as json_file:
            json.dump(data, json_file)
        return 'exported_data.json'
    elif format_type == 'excel':
        df = pd.DataFrame(data)
        df.to_excel('exported_data.xlsx', index=False)
        return 'exported_data.xlsx'
    else:
        raise ValueError(f"Format d'exportation '{format_type}' non supporté.")
