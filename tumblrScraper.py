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
    for size in photo["alt_sizes"]:
        url = size["url"]
        req = requests.get(url)
        if req.status_code == 200:
            with open(url.split("/")[-1], 'wb') as f:
                for chunk in req.iter_content():
                    f.write(chunk)
            return True
    return False


def save_post_photo(post):
    dir = post["date"].split(" ")[1]
    os.mkdir(dir)
    os.chdir(dir)
    for photo in post["photos"]:
        if save_photo(photo):
            break
    os.chdir("..")


def save_post_audio(post):
    with open(post["artist"] + " - " + post["track_name"] + ".jpg", 'wb') as f:
        url = post["album_art"]
        req = requests.get(url)
        for chunk in req.iter_content():
            f.write(chunk)


def save_post(post):
    dir = post["date"].split(" ")[0]
    if not os.path.isdir(dir):
        os.mkdir(dir)
    os.chdir(dir)
    if post["type"] == "text":
        save_post_text(post)
    elif post["type"] == "photo":
        save_post_photo(post)
    elif post["type"] == "audio":
        save_post_audio(post)
    os.chdir("..")


def save_page(page):
    page_data = page.json()
    for post in page_data["response"]["posts"]:
        save_post(post)


for i in range(0, 20, 20):
    page = requests.get(
        "http://api.tumblr.com/v2/blog/missdania.tumblr.com/posts?api_key=UjoFgpzdX0omRQKeitBRInTlIkQOUpa5z24ZuFCRYW2fzefEeY&offset=" + str(i))
    save_page(page)