import os
import subprocess
import os.path

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

working_dir = "/tmp/the-great-archiving"
ORG = "cf-platform-eng"

def run_command(cmd, dir=None):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=dir)
    out, err = p.communicate()
    if p.returncode != 0:
        print("Failed running command:")
        print(cmd)
        print(out.decode('utf8'))
        print(err.decode('utf8'))
        raise Exception("Failed running command")

    return out.decode('utf8')

def main():
    token = os.environ.get("ACCESS_TOKEN", None)
    if not token:
        raise Exception("Token environment variable is required")

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
        {{
          search(query: "org:{} is:public archived:false", type: REPOSITORY, first: 100) {{
            repositoryCount
            edges {{
              node {{
                ... on Repository {{
                  id
                  name
                  isArchived
                  isPrivate
                  owner {{
                    id
                    login
                  }}
                  codeOfConduct {{
                    key
                    name
                    url
                  }}
                }}
              }}
            }}
          }}
        }}
    """.format(ORG)

    # List of public, non-archived repos
    result = client.execute(gql(get_id_query))
    print(result, "\n\n")
    print(result["search"]["edges"], "\n\n")

    with open("CODE-OF-CONDUCT.md") as conduct_file:
        code_of_conduct = conduct_file.read()

    for repo in result["search"]["edges"]:
        print(repo)

        # Build repo name
        repo_name = repo["node"]["name"]
        # run_command("git clone http://github.com/{}/{}".format(ORG, repo_name), working_dir)
        run_command("git clone git@github.com:{}/{}".format(ORG, repo_name), working_dir)

        conduct_name = "CODE-OF-CONDUCT.md"
        repo_path = os.path.join(working_dir, repo_name)
        conduct_path = os.path.join(repo_path, conduct_name)
        conduct_exists = os.path.isfile(conduct_path)

        if not conduct_exists:
            print("Adding license to {}".format(repo_name))
            with open(conduct_path, 'w') as code_of_conduct_file:
                code_of_conduct_file.write(code_of_conduct)

            # commit locally
            print(run_command("git add {}".format(conduct_name), repo_path))
            print(run_command("git commit -m 'Add license {}'".format(conduct_name), repo_path))

            # push
            print(run_command("git push", repo_path))

            # os.sys.exit(0)

if __name__ == '__main__':
    main()
