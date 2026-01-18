# md_to_html.py
import markdown
import os

# 读取生成的文章
with open("latest_digest.md", "r") as f:
    md_content = f.read()

# 转换为 HTML
html_content = markdown.markdown(md_content, extensions=['fenced_code'])

# 添加精美样式
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech English Weekly</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }}
        h2 {{
            color: #1a73e8;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .header h1 {{
            color: #2c3e50;
            font-size: 28px;
        }}
        @media (prefers-color-scheme: dark) {{
            body {{
                background: #1e1e1e;
                color: #e0e0e0;
            }}
            h2 {{
                color: #64b5f6;
                border-color: #444;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Weekly Tech English Digest</h1>
        <p>Auto-generated for English learning • Updated weekly</p>
    </div>
    {html_content}
</body>
</html>
"""

# 保存到 output 目录
os.makedirs("output", exist_ok=True)
with open("output/index.html", "w") as f:
    f.write(full_html)

print("✅ HTML 已生成到 output/index.html")
