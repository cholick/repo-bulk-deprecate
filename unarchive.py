import os

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# from repos_small import repos
from repos_full import repos

ORG = "cf-platform-eng"


def main():
    token = os.environ.get("ACCESS_TOKEN", None)
    if not token:
        raise Exception("Token environment variable is required")

    for repo_url in repos:
        repo_name = repo_url.split("/")[-1]
        full_repo_name = ORG + "/" + repo_name
        print("Getting repo {}".format(full_repo_name))

        reqHeaders = {
            'Authorization': 'Bearer ' + token
        }
        transport = RequestsHTTPTransport(
            url="https://api.github.com/graphql",
            headers=reqHeaders,
            use_json=True,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        get_id_query = """
            query FindRepoID {{
                repository(owner:"{}", name:"{}"){{
                    id, name
                }}
            }}
        """.format(ORG, repo_name)

        result = client.execute(gql(get_id_query))
        print(result)
        repo_id = result["repository"]["id"]

        print("Unarchiving {}".format(repo_name))
        unarchive_query = """
        mutation UnArchiveRepository {{
            unarchiveRepository(input:{{ clientMutationId:"true", repositoryId: "{}"}}) {{
                repository {{
                    isArchived,
                }}
            }}
        }}
        """.format(repo_id)

        result = client.execute(gql(unarchive_query))
        print(result)


if __name__ == '__main__':
    main()
