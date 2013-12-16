import os
import requests

req = requests.get(
    "http://api.tumblr.com/v2/blog/missdania.tumblr.com/info?api_key=UjoFgpzdX0omRQKeitBRInTlIkQOUpa5z24ZuFCRYW2fzefEeY")
data = req.json()

number_of_posts = data["response"]["blog"]["posts"]

os.mkdir("Posts")
os.chdir("Posts")


def save_post_text(post):
    with open(post["slug"] + ".txt", 'w') as f:
        f.write("Date: %s\n\n" % post["date"].encode('utf8'))
        f.write("URL: %s\n\n" % post["post_url"].encode('utf8'))
        f.write("Notes: %s\n\n" % post["note_count"])
        f.write(post["body"].encode('utf8') + '\n\n')
        if post["tags"]:
            f.write("Tags:\n\n")
            for tag in post["tags"]:
                f.write(tag.encode('utf8') + '\n')


def save_photo(photo):
    req = requests.get(photo["original_size"]["url"])
    if req.status_code == 200:
        


def save_post_photo(post):
    dir = post["date"].split(" ")[1]
    os.mkdir(dir)
    os.chdir(dir)
    for photo in post["photos"]:
        save_photo(photo)
    os.chdir("..")


def save_post(post):
    dir = post["date"].split(" ")[0]
    if not os.path.isdir(dir):
        os.mkdir(dir)
    os.chdir(dir)
    if post["type"] == "text":
        save_post_text(post)
    elif post["type"] == "photo":
        save_post_photo(post)
    os.chdir("..")


def save_page(page):
    page_data = page.json()
    for post in page_data["response"]["posts"]:
        save_post(post)


for i in range(0, 20, 20):
    page = requests.get(
        "http://api.tumblr.com/v2/blog/missdania.tumblr.com/posts?api_key=UjoFgpzdX0omRQKeitBRInTlIkQOUpa5z24ZuFCRYW2fzefEeY&offset=" + str(i))
    save_page(page)