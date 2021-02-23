import os
import requests

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from repos_small import repos

SOURCE_ORG = "cf-platform-eng"
TARGET_ORG = "vmware-archive"

def main():
    token = os.environ.get("ACCESS_TOKEN", None)
    if not token:
        raise Exception("Token environment variable is required")

    request_headers = {
        'Authorization': 'Bearer ' + token
    }

    # Setup GraphQL API
    graphql_transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers=request_headers,
        use_json=True,
    )
    client = Client(transport=graphql_transport, fetch_schema_from_transport=True)

    # Setup REST API Transfer request
    # https://api.github.com/repos/{owner}/{repo}/transfer
    rest_query_url = "https://api.github.com/repos/{}/{}/transfer"
    rest_payload = """
    {{
        "new_owner":"{}"
    }}
    """

    # Modify this search query to select only the repos you want to transfer, see comment at bottom of file.
    print("Get Public Archived Repos for source org {}".format(SOURCE_ORG))
    get_public_archived_repos_query = """
        {{
          search(query: "org:{} is:public archived:true fork:false", type: REPOSITORY, first: 100) {{
            repositoryCount
            edges {{
              node {{
                ... on Repository {{
                    id
                    name
                    url
                    owner {{
                        id
                        login
                    }}
                    licenseInfo {{
                        id
                        name
                    }}
                }}
              }}
            }}
          }}
        }}
    """.format(SOURCE_ORG)

    archived_repos = client.execute(gql(get_public_archived_repos_query))

    repos_without_license = []

    input("Validate Source ({}) and Target ({}) Org are correct, then press ENTER to transfer {} repositories".format(SOURCE_ORG, TARGET_ORG, archived_repos["search"]["repositoryCount"]))

    for edge in archived_repos["search"]["edges"]:
        repo = edge["node"]
        # print(repo)

        if repo["licenseInfo"] == None:
            print("NO license found for '{}:{}', not transferring".format(repo["owner"]["login"],repo["name"]))
            repos_without_license.append(repo["name"])
        else:
            print("License found, changing repo '{}' owner from '{}' to '{}'".format(repo["name"], repo["owner"]["login"], TARGET_ORG))
            # print("Transfer request URI: " + rest_query_url.format(repo["owner"]["login"], repo["name"]))
            # print("Transfer request data: " + rest_payload.format(TARGET_ORG))
            resp = requests.post(
                rest_query_url.format(repo["owner"]["login"], repo["name"]),
                data=rest_payload.format(TARGET_ORG),
                headers=request_headers
            )
            print("Response code '{} : {}' for repo '{}'".format(resp.status_code, resp.reason, repo["name"]))

    if len(repos_without_license) > 0:
        print("{} repositories NOT moved due to no license: {}".format(len(repos_without_license), repos_without_license))


if __name__ == '__main__':
    main()

# To experiment with GitHub GraphQL API and modify this search for your purposes:
#  - Uncomment the `query Find Archived` json
#  - Go to https://docs.github.com/en/graphql/overview/explorer
#  - Paste it in query textarea
#
# NOTE: This `search query` is used by the GitHub search box, so the query string
#   "org:cf-platform-eng is:public archived:true fork:false" can be pasted directly the
#   search box.
#
# For more info on advanced GitHub searching see the docs:
# https://docs.github.com/en/github/searching-for-information-on-github
#
# query FindArchived {
#   search(
#     query: "org:cf-platform-eng is:public archived:true fork:false",
#     type: REPOSITORY, first: 100) {
#     repositoryCount
#     edges {
#       node {
#         ... on Repository {
#           id
#           name
#           isArchived
#           isPrivate
#           isFork
#           url
#           owner {
#             id
#             login
#           }
#           licenseInfo {
#             id
#             name
#           }
#         }
#       }
#     }
#   }
# }