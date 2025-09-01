# In blog/ssg.py

import os
import markdown
from datetime import datetime

# --- CONFIGURATION ---
# Get the absolute path of the directory containing this script (ogbox/blog/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
# Get the root project directory (ogbox/)
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

POSTS_DIR = os.path.join(ROOT_DIR, "blog", "posts")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "blog", "templates")
# Output will be in the main 'blog' folder
OUTPUT_DIR = os.path.join(ROOT_DIR, "blog")

def main():
    print(f"Looking for posts in: {POSTS_DIR}")
    print(f"Using templates from: {TEMPLATES_DIR}")
    print(f"Writing output to: {OUTPUT_DIR}")

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get all blog posts
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(POSTS_DIR, filename), "r") as f:
                content = f.read()
                
                lines = content.split('\n')
                # Basic error checking
                if len(lines) < 3 or not lines[0].startswith('title:') or not lines[1].startswith('image:'):
                    print(f"WARNING: Skipping malformed post: {filename}")
                    continue

                title = lines[0].replace('title: ', '').strip()
                image_url = lines[1].replace('image: ', '').strip()
                
                body_md = '\n'.join(lines[2:]).strip()
                body_html = markdown.markdown(body_md, extensions=['fenced_code'])

                slug = os.path.splitext(filename)[0]
                post_filename = f"{slug}.html"
                
                creation_time = os.path.getmtime(os.path.join(POSTS_DIR, filename))
                post_date = datetime.fromtimestamp(creation_time)

                posts.append({
                    "title": title,
                    "image_url": image_url,
                    "body_html": body_html,
                    "filename": post_filename,
                    "date": post_date
                })

    if not posts:
        print("No markdown posts found. Exiting.")
        return

    posts.sort(key=lambda x: x["date"], reverse=True)

    # Generate individual blog post pages
    with open(os.path.join(TEMPLATES_DIR, "blog_post.html"), "r") as f:
        post_template = f.read()

    for post in posts:
        post_html = post_template.replace("{{title}}", post["title"])
        post_html = post_html.replace("{{image_url}}", post["image_url"])
        post_html = post_html.replace("{{body}}", post["body_html"])
        post_html = post_html.replace("{{publish_date}}", post["date"].strftime("%B %d, %Y"))

        with open(os.path.join(OUTPUT_DIR, post["filename"]), "w") as f:
            f.write(post_html)
        print(f"Generated: {post['filename']}")


    # Generate the blog index page
    with open(os.path.join(TEMPLATES_DIR, "index.html"), "r") as f:
        index_template = f.read()

    post_links_html = ""
    for post in posts:
        formatted_date = post['date'].strftime('%-m-%-d-%y') # Use %-m and %-d to remove leading zeros
        post_links_html += f'<li><a href="{post["filename"]}">{formatted_date} - {post["title"]}</a></li>\n'
    
    final_index_html = index_template.replace("{{posts_list}}", post_links_html)

    # Note: This will overwrite the template placeholder, not create a new file
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(final_index_html)
    print("Generated: blog/index.html")


if __name__ == "__main__":
    main()
