import os
import re
count = 0
for root, dirs, files in os.walk('frontend'):
    for file in files:
        if file.endswith('.html'):
            f = os.path.join(root, file)
            try:
                with open(f, 'r', encoding='utf-8') as file_obj:
                    content = file_obj.read()
                if 'script.js?v=' in content:
                    new_content = re.sub(r'script\.js\?v=\d+\.\d+', 'script.js?v=3.3', content)
                    if new_content != content:
                        with open(f, 'w', encoding='utf-8') as file_obj:
                            file_obj.write(new_content)
                        count += 1
            except Exception as e:
                pass
print(f'Done. Updated {count} files.')
