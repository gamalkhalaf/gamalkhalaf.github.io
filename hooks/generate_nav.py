import os

EXCLUDE = {'admin', 'assets', 'javascripts', 'overrides'}

def _get_title(filepath):
    if not os.path.isfile(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()
        if not content.startswith('---'):
            return None
        end = content.find('---', 3)
        if end == -1:
            return None
        meta = content[3:end]
        for line in meta.split('\n'):
            line = line.strip()
            if line.startswith('title:'):
                return line.split(':', 1)[1].strip().strip('"').strip("'")
    return None

def _section_entries(dirpath, prefix):
    entries = []
    for f in sorted(os.listdir(dirpath)):
        if not f.endswith('.md'):
            continue
        title = _get_title(os.path.join(dirpath, f))
        if title is None:
            title = os.path.splitext(f)[0]
        entries.append({title: f'{prefix}/{f}'})
    return entries

def on_config(config):
    docs_dir = config['docs_dir']

    nav = [
        {'الرئيسية': 'index.md'},
    ]

    for d in sorted(os.listdir(docs_dir)):
        dirpath = os.path.join(docs_dir, d)
        if not os.path.isdir(dirpath) or d in EXCLUDE:
            continue
        if not any(f.endswith('.md') for f in os.listdir(dirpath)):
            continue

        entries = _section_entries(dirpath, d)
        if not entries:
            continue

        section_title = _get_title(os.path.join(dirpath, 'index.md'))
        if section_title is None:
            section_title = d
        nav.append({section_title: entries})

    config['nav'] = nav
    return config
