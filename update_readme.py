import subprocess
import os.path

# from repos_small import repos
from repos_full import repos

working_dir = "/tmp/the-great-archiving"

archive_text_markdown = "# {} is no longer actively maintained by VMware.\n\n"


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
    run_command("mkdir -p {}".format(working_dir))

    for repo in repos:
        print("Handing {}".format(repo))
        # path might need tweaking based on how one clones, my machine uses https method rather than ssh

        run_command("git clone http://{}".format(repo), working_dir)
        paths = repo.split("/")
        repo_name = paths[-1]

        readme_name = "README.md"
        repo_path = os.path.join(working_dir, repo_name)
        readme_path = os.path.join(repo_path, readme_name)
        readme_exists = os.path.isfile(readme_path)
        if readme_exists:
            print("UPDATING readme to {}".format(repo_name))
            with open(readme_path, 'r+') as readme_file:
                content = readme_file.read()
                readme_file.seek(0, 0)
                readme_file.write(archive_text_markdown.format(repo_name))
                readme_file.write(content)
        else:
            print("ADDING readme to {}".format(repo_name))
            with open(readme_path, 'w') as readme_file:
                readme_file.write(archive_text_markdown.format(repo_name))

        # commit locally
        print(run_command("git add {}".format(readme_name), repo_path))
        print(run_command("git commit -m 'Add archive text to {}'".format(readme_name), repo_path))
        # push
        print(run_command("git push", repo_path))


if __name__ == '__main__':
    main()
