import os
import re

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix all head favicon links
            content = re.sub(r'<link rel="icon".*?>', '', content)
            content = re.sub(r'<link rel="apple-touch-icon".*?>', '', content)
            
            # Insert standard favicon links before </head>
            favicon_links = '\n  <link rel="icon" type="image/png" sizes="64x64" href="assets/icons/favicon.png">\n  <link rel="apple-touch-icon" href="assets/icons/favicon.png">\n</head>'
            content = content.replace('</head>', favicon_links)
            
            # Clean up empty lines created by removing links
            content = re.sub(r'\n\s*\n\s*</head>', '\n</head>', content)

            # Fix logo tag if it was messed up (index.html had <link> tags inside logo)
            logo_pattern = r'<a href="index.html" class="logo">.*?</a>'
            correct_logo = '<a href="index.html" class="logo">\n        <img src="assets/icons/favicon.png" alt="Swiftsitedev Logo" class="logo-img">\n        <span>Swift<span>Sitedev</span><b>.</b></span>\n      </a>'
            
            content = re.sub(logo_pattern, correct_logo, content, flags=re.DOTALL)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {path}')
