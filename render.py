from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml
import shutil

# Set up the environment
env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=False # All our data comes from trusted sources
)

# Iterate over all the language YAML files in the static_content directory
# and create a new HTML file for each one.
languages = [p.stem for p in Path('./content').glob('*.yaml')]
for p in Path('./content').glob('*.yaml'):
    with open(p, 'r') as f:
        data = yaml.safe_load(f)

    # Add language specific data
    data['language'] = {
        'current': p.stem,
        'available': languages
    }

    # Render the template with data
    output = env.get_template('index.html').render(data)

    # Write the output to an HTML file
    html = Path('./output') / p.stem / 'index.html'
    html.parent.mkdir(parents=True, exist_ok=True)
    with open(html, 'w', encoding='utf-8') as f:
        f.write(output)

# Copy the static directory to the output directory
shutil.copytree('./static', './output/static', dirs_exist_ok=True)