import os
import sys
import yaml
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECTS_DIR = os.path.join(ROOT, 'docs', 'admin', 'subjects')
CONFIG_PATH = os.path.join(ROOT, 'docs', 'admin', 'config.yml')


def main():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        existing = yaml.safe_load(f)

    subject_files = sorted(glob.glob(os.path.join(SUBJECTS_DIR, '*.yml')))

    new_config = {
        'backend': existing['backend'],
        'media_folder': existing['media_folder'],
        'public_folder': existing['public_folder'],
        'collections': [],
    }

    for coll in existing.get('collections', []):
        if coll.get('name') == 'subjects':
            coll['extension'] = 'yml'
            coll['format'] = 'yaml'
            coll['slug'] = '{{fields.slug}}'
            new_config['collections'].append(coll)
            break

    for sf in subject_files:
        with open(sf, 'r', encoding='utf-8') as f:
            subject = yaml.safe_load(f)

        slug = subject['slug']
        label = subject['label']

        subject_dir = os.path.join(ROOT, 'docs', slug)
        index_path = os.path.join(subject_dir, 'index.md')
        if not os.path.exists(index_path):
            os.makedirs(subject_dir, exist_ok=True)
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(f'---\ntitle: {label}\n---\n\n# {label}\n\n')

        new_config['collections'].append({
            'name': f'{slug}_lessons',
            'label': label,
            'folder': f'docs/{slug}',
            'create': True,
            'slug': '{{slug}}',
            'fields': [
                {'label': 'عنوان الدرس', 'name': 'title', 'widget': 'string'},
                {'label': 'تفعيل التشفير وحماية الصفحة', 'name': 'encrypt', 'widget': 'boolean', 'default': True},
                {'label': 'محتوى الدرس', 'name': 'body', 'widget': 'markdown'},
            ],
        })

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(new_config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f'Generated config.yml with {len(subject_files)} subjects')


if __name__ == '__main__':
    main()
