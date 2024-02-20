from jinja2 import Environment, FileSystemLoader
import yaml, shutil
from pathlib import Path
from util_images import process_images_and_generate_html
from util_gsheet import read_gsheet_data
from datetime import datetime

def main():
    # Create the Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'), autoescape=False)
    
    # Read the name of all yaml files in content directory, which indicate the languages.
    # Do this only once, as the languages are the same for all pages.
    languages = [p.stem for p in Path('./content').glob('*.yaml')]

    # Read events and organiser data from Google Sheets. 
    # These lists are language independent, so we only need to read them once.
    events_data, organisers_data = read_gsheet_data()
    
    for p in Path('./content').glob('*.yaml'):
        with open(p, 'r') as f:
            data = yaml.safe_load(f)

        # Add events and organisers data
        data['events'] = events_data
        data['organisers'] = organisers_data

        html_output = Path('./output') / p.stem / 'index.html'
        # Modify data in-place to add a key img_html for each specified image. Ugly wbut works for now.
        process_images_and_generate_html(data, './output/static/img', [320, 480, 640, 768, 992, 1200, 1400, 1600, 1920], html_output)
        
         # Add timestamp of today in format dd.mm.yy
        data['processed_asof'] = datetime.now().strftime('%d.%m.%y')

        # Add language data
        data['language'] = {'current': p.stem, 'other_available': [l for l in languages if l != p.stem]}

        # Render HTML and write the output to a file
        output = env.get_template('index.html').render(data)
        html_output.parent.mkdir(parents=True, exist_ok=True)
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(output)

    # Copy static files to output
    shutil.copytree('./static', './output/static', dirs_exist_ok=True)

    # Write a dummy index.html to output root that redirects to german if available, otherwise to the first language.
    with open('./output/index.html', 'w', encoding='utf-8') as f:
        inital_language = "de" if "de" in languages else languages[0]
        f.write(f'<meta http-equiv="refresh" content="0; url=./{inital_language}">')
    

if __name__ == "__main__":
    main()
