# repo-bulk-deprecate
This is a quick set of scripts to for working with GitHub repositories.

## Scripts
* `update_readme.py` pre-pend to a message to the top of the `README.md` file that this repo is no longer actively maintained.
* `archive.py` archives via the GitHub API (using the `ACCESS_TOKEN` environment variable)
* `unarchive.py` unarchives via the GitHub API (using the `ACCESS_TOKEN` environment variable)
* `add_license.py` adds the [LICENSE](LICENSE) file to the repo if it does not exist.
* `add_code_of_conduct.py` uses the GitHub GraphQL API to retrieve a list of public, non-archived repositories for the given organization (using the `ACCESS_TOKEN` environment variable) and adds [CODE-OF-CONDUCT.md](CODE-OF-CONDUCT.md) if it does not exist.
* `move_repop.py` uses the GitHub GraphQL API to retrieve a list of public, archived, non-fork repositories for the given SOURCE organization, iterates through them and if they have a License, used the GitHub REST API to transfer them to the TARGET organziation.

Be sure to run updating the README first, as once it's archived, it can no longer be updated
without first unarchiving.

Various constants are hard-coded in the python files.
* `repos_full.py` is the full list of repositories to archive
* `repos_small.py` is a smaller list (should be disjoint) to test with. Committed files are importing the full list.

## Access Token
To create the ACCESS_TOKEN go to https://github.com/settings/tokens and give it `repo` scope.

## Editors
### VScode / VSCodium:
- Paste the ACCESS_TOKEN into `token.env`
- Create a launch configuration with an `envFile` like shown below:
  ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "envFile": "${workspaceFolder}/token.env",
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            }
        ]
    }
  ```