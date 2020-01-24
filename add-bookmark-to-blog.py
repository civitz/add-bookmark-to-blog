from github import Github
from datetime import date
import os
import yaml
import sys
import argparse

# or using an access token

def login ():
    "login to github, use access token from environment"
    gh_access_token=os.environ['GH_ADD_BOOKMARK_ACCESS_TOKEN']
    return Github(gh_access_token)

def get_blog (github_login):
    return github_login.get_repo("civitz/civitz.github.io")

def file_content(link, description, short=None, publish=True, tags=[]):
    parts={
        'published': publish,
        'link': link
    }
    if short != None:
        parts['short']=short
    if tags != None and tags:
        parts['tags']=tags
    print (parts)
    yaml_front_matter = yaml.dump(parts)
    return "---\n" + yaml_front_matter + "---\n\n" + description + "\n"

def file_name(date, name):
    return date.strftime("%Y-%m-%d-") + name.replace(" ","-") + ".md"

def add_link_to_blog(link, name, description, short=None, publish=True, tags=[], dryrun=False):
    filename = file_name(date.today(), name.lower())
    print ("Resulting file name: " + filename)
    content = file_content(link,description, publish=publish,short=short, tags=tags)
    print ("Resulting file content: ")
    print (content)
    if dryrun:
        print ("Here we would have created a file on the blog")
    else:
        print("logging in")
        gh=login()
        blog=get_blog(gh)
        result = blog.create_file(path="_bookmarks/"+filename, content=content,branch="netlify",message="Adding " + filename)
        print ("Result: ")
        print (result)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("link",
                        help="the link to publish")
    parser.add_argument("-n", "--name",
                        help="file name")
    parser.add_argument("-s", "--short",
                        help="Short name for page")
    parser.add_argument("-d", "--description",
                        help="Link description")
    parser.add_argument("-t", "--tags", action="append",
                        help="Tag list")
    parser.add_argument("-p", "--publish", action="store_true",
                        help="immediately publish")
    parser.add_argument("--dryrun", action="store_true",
                        help="don't publish to github")
    parsed = parser.parse_args(argv)
    print parsed
    if parsed.description == None:
        print ("Missing description parameter")
        sys.exit(1)
    if parsed.name == None:
        print ("Missing name parameter")
        sys.exit(1)
    add_link_to_blog(link=parsed.link, name=parsed.name,
                     description=parsed.description, short=parsed.short,
                     publish=parsed.publish, tags=parsed.tags, dryrun=parsed.dryrun)

if __name__ == "__main__":
   main(sys.argv[1:])

def lambda_handler(event, context):
    print('## EVENT')
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }