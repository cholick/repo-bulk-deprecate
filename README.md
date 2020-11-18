# repo-bulk-deprecate

This is a quick script to deprecate a collection of repositories.
* `update_readme.py` pre-pend to a message to the top of the `README.md` file 
* `archive.py` does the archiving via the GitHub API (using the `ACCESS_TOKEN` environment variable)
* `unarchive.py` unarchives via the GitHub API (using the `ACCESS_TOKEN` environment variable)

Be sure to run updating the README first, as once it's archived, it can no longer be updated
without first unarchiving.

Various constants are hard-coded in the two python files.
* `repos_full.py` is the full list of repositories
* `repos_small.py` is a smaller list (should be disjoint) to test with. Committed files are importing the full list.  

