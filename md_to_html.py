import re
import sys

def convert_markdown_to_html(markdown_text):
    html_lines = []
    in_list = False

    for line in markdown_text.split("\n"):
        line = line.strip()

        # Skip empty lines
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Headers (##, #)
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")

        # List Items (- item)
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")

        else:
            # Apply inline formatting to paragraphs
            formatted = line
            formatted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", formatted)  # bold
            formatted = re.sub(r"\*(.+?)\*", r"<em>\1</em>", formatted)              # italics
            formatted = re.sub(r"`(.+?)`", r"<code>\1</code>", formatted)            # inline code
            formatted = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', formatted)  # links
            html_lines.append(f"<p>{formatted}</p>")

    if in_list:
        html_lines.append("</ul>")  # Close list if still open

    return "\n".join(html_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python md_to_html.py input.md output.html")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    html_content = convert_markdown_to_html(md_content)

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"✅ Converted '{input_path}' to '{output_path}' successfully!")

if __name__ == "__main__":
    main()
