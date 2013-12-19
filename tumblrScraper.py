import os
import requests

req = requests.get(
    "http://api.tumblr.com/v2/blog/missdania.tumblr.com/info?api_key=UjoFgpzdX0omRQKeitBRInTlIkQOUpa5z24ZuFCRYW2fzefEeY")
data = req.json()

number_of_posts = data["response"]["blog"]["posts"]

root_dir = "Posts"

os.mkdir(root_dir)
os.chdir(root_dir)
os.mkdir("Text & Quote")
os.mkdir("Photo")
os.mkdir("Chat")

def save_aux(post, f):
    f.write("Date: %s\n\n" % post["date"].encode('utf8'))
    if "note_count" in post:
        f.write("Notes: %s\n\n" % post["note_count"])
    if post["tags"]:
        f.write("Tags:\n\n")
        for tag in post["tags"]:
            f.write(tag.encode('utf8') + '\n')
        f.write('\n\n')


def make_dir(post):
    dir = post["date"].split(" ")[0]
    if not os.path.isdir(dir):
        os.mkdir(dir)
    os.chdir(dir)


def save_post_text(post):
    os.chdir("Text & Quote")
    make_dir(post)
    with open(post["slug"] + ".txt", 'w') as f:
        save_aux(post, f)
        if post["type"] == "text":
            f.write(post["body"].encode('utf8') + '\n\n')
        else:
            f.write(post["text"].encode('utf8') + '\n\n')


def save_photo(post, date, number):
    for size in post["alt_sizes"]:
        url = size["url"]
        req = requests.get(url)
        if req.status_code == 200:
            with open(date + " - " + str(number) + "." + url.split(".")[-1], 'wb') as f:
                for chunk in req.iter_content():
                    f.write(chunk)
            return True
    return False


def save_post_photo(post):
    os.chdir("Photo")
    make_dir(post)
    dir = post["date"].split(" ")[1]
    os.mkdir(dir)
    os.chdir(dir)
    for photo in post["photos"]:
        if save_photo(photo, post["date"], post["photos"].index(photo)):
            continue
    with open(post["date"].split(" ")[1] + ".txt", 'w') as f:
        save_aux(post, f)
        if post["caption"] != "":
            f.write('%s\n\n' % post["caption"])
    os.chdir("..")


def save_post_chat(post):
    os.chdir("Chat")
    make_dir(post)
    with open(post["slug"] + ".txt", 'w') as f:
        save_aux(post, f)
        for comment in post["body"].split("\r\n"):
            f.write("%s\n\n" % comment.encode('utf8'))


def save_post(post):
    if post["type"] in ["text", "quote"]:
        save_post_text(post)
    elif post["type"] == "photo":
        save_post_photo(post)
    elif post["type"] == "chat":
        save_post_chat(post)
    else:
        return 
    os.chdir("../..")


def save_page(page):
    page_data = page.json()
    for post in page_data["response"]["posts"]:
        save_post(post)


for i in range(0, 20, 20):
    page = requests.get(
        "http://api.tumblr.com/v2/blog/missdania.tumblr.com/posts?api_key=UjoFgpzdX0omRQKeitBRInTlIkQOUpa5z24ZuFCRYW2fzefEeY&offset=" + str(i))
    save_page(page)

os.chdir("..")
os.system("zip -r Tumblr\ Archive.zip %s" % root_dir)