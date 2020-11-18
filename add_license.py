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
    with open("LICENSE") as apache2_license_file:
        apache2_license = apache2_license_file.read()

    run_command("mkdir -p {}".format(working_dir))

    for repo in repos:
        print("Handing {}".format(repo))

        # path might need tweaking based on how one clones, my machine uses https method rather than ssh
        run_command("git clone http://{}".format(repo), working_dir)
        paths = repo.split("/")
        repo_name = paths[-1]

        license_name = "LICENSE"
        repo_path = os.path.join(working_dir, repo_name)
        license_path = os.path.join(repo_path, license_name)
        license_exists = os.path.isfile(license_path)
        if not license_exists:
            print("Adding license to {}".format(repo_name))
            with open(license_path, 'w') as license_file:
                license_file.write(apache2_license)

            # commit locally
            print(run_command("git add {}".format(license_name), repo_path))
            print(run_command("git commit -m 'Add license {}'".format(license_name), repo_path))
            # push
            print(run_command("git push", repo_path))


if __name__ == '__main__':
    main()
