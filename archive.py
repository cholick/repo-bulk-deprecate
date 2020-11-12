import os

from github import Github

# from repos_small import repos
from repos_full import repos

ORG = "cf-platform-eng"


def main():
    # or using an access token
    token = os.environ.get("ACCESS_TOKEN", None)
    if not token:
        raise Exception("Token environment variable is required")

    g_api = Github(token)

    for repo_url in repos:
        repo_name = repo_url.split("/")[-1]
        full_repo_name = ORG + "/" + repo_name
        print("Getting repo {}".format(full_repo_name))
        repo = g_api.get_repo(full_repo_name)
        if not repo.archived:
            print("Archiving {}".format(repo_url))
            repo.edit(archived=True)
        else:
            print("{} is already archived, not taking action".format(repo_url))


if __name__ == '__main__':
    main()
