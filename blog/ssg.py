import os
import markdown
from datetime import datetime

# Configuration
POSTS_DIR = "blog/posts"
OUTPUT_DIR = "blog"
TEMPLATES_DIR = "blog/templates"

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get all blog posts
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(POSTS_DIR, filename), "r") as f:
                content = f.read()
                
                # Simple front matter parsing
                lines = content.split('\n')
                title = lines[0].replace('title: ', '').strip()
                image_url = lines[1].replace('image: ', '').strip()
                
                # Get the rest of the content for Markdown conversion
                body_md = '\n'.join(lines[2:]).strip()
                body_html = markdown.markdown(body_md)

                # Generate HTML filename
                slug = os.path.splitext(filename)[0]
                post_filename = f"{slug}.html"
                
                # For simplicity, we'll use the file's creation date.
                # A more robust solution might use a date in the front matter.
                creation_time = os.path.getmtime(os.path.join(POSTS_DIR, filename))
                post_date = datetime.fromtimestamp(creation_time)

                posts.append({
                    "title": title,
                    "image_url": image_url,
                    "body_html": body_html,
                    "filename": post_filename,
                    "date": post_date
                })

    # Sort posts by date, newest first
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

    # Generate the blog index page
    with open(os.path.join(TEMPLATES_DIR, "index.html"), "r") as f:
        index_template = f.read()

    post_links_html = ""
    for post in posts:
        # We format the date to match your example (e.g., 8-14-25)
        formatted_date = post['date'].strftime('%m-%d-%y')
        post_links_html += f'<li><a href="{post["filename"]}">{formatted_date} - {post["title"]}</a></li>\n'
    
    final_index_html = index_template.replace("{{posts_list}}", post_links_html)

    # We name it blog.html to avoid conflict with your main index.html
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(final_index_html)

if __name__ == "__main__":
    main()
