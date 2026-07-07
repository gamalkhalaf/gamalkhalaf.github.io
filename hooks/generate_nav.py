import os

def on_config(config):
    docs_dir = config['docs_dir']
    nahw_dir = os.path.join(docs_dir, 'nahw')

    nahw_entries = []

    if os.path.isdir(nahw_dir):
        for f in sorted(os.listdir(nahw_dir)):
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(nahw_dir, f)
            title = None
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end != -1:
                        meta = content[3:end]
                        for line in meta.split('\n'):
                            line = line.strip()
                            if line.startswith('title:'):
                                title = line.split(':', 1)[1].strip().strip('"').strip("'")
                                break
            if title is None:
                title = os.path.splitext(f)[0]
            nahw_entries.append({title: f'nahw/{f}'})

    nav = [
        {'الرئيسية': 'index.md'},
    ]

    if nahw_entries:
        nav.append({'دروس في النحو': nahw_entries})

    config['nav'] = nav
    return config
