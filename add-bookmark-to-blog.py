from github import Github
from datetime import date
import os
import yaml

# or using an access token

def login ():
    "login to github, use access token from environment"
    gh_access_token=os.environ['GH_ADD_BOOKMARK_ACCESS_TOKEN']
    return Github(gh_access_token)

def get_blog (github_login):
    return github_login.get_repo("civitz/civitz.github.io")

def file_content(link, description, short=None, publish=True, tags=[]):
    yfm="---\n"
    parts={
        'published': publish,
        'link': link
    }
    if short != None:
        parts['short']=short
    if tags != None and tags:
        parts['tags']=tags
    yaml_front_matter = yaml.dump(parts)
    return "---\n" + yaml_front_matter + "---\n\n" + description + "\n"

def file_name(date, name):
    return date.strftime("%Y-%m-%d-") + name.replace(" ","-") + ".md"


def add_link_to_blog(link, name, description, short=None, publish=True, tags=[])
    print("logging in")
    gh=login()
    blog=get_blog(gh)
    filename = file_name(date.today(), name.lower()))
    print ("Resulting file name: " + filename)
    content = file_content(link,description, publish=False)
    print ("Resulting file content: " + content)
    result = blog.create_file(path="_bookmarks/"+filename, content=content,branch="netlify",message="Adding " + filename)
    print ("Result: ")
    print result

def lambda_handler(event, context):
    print('## EVENT')
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }