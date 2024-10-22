[positional-arguments]
pin python_version:
    rye pin {{python_version}} --relaxed
    rye sync
    rye test

[positional-arguments]
update_workflow minimum_version maximum_version:
    #! /usr/bin/env python3
    from pathlib import Path
    import sys

    workflows = [Path('.github/workflows/package_testing.yml'), Path('.github/workflows/release_on_pypi.yml')]

    vmin = sys.argv[1]
    vmax = sys.argv[2]

    minor_min = int(vmin.split(".")[1])
    minor_max = int(vmax.split(".")[1])

    for workflow in workflows:
        with open(workflow) as f:
            content = f.readlines()

        for it, line in enumerate(content):
            if "MAIN_PYTHON_VERSION: " in line:
                print(it)
                content[it] = f'  MAIN_PYTHON_VERSION: "{vmax}"\n'
            elif "python-version:" in line:
                new_line = f'        python-version: ['
                for jt in range(minor_min, minor_max):
                    new_line += f'"3.{jt}", '
                new_line += f'"3.{minor_max}"]\n'
                content[it] = new_line

        with open(workflow, 'w') as f:
            f.writelines(content)

[positional-arguments]
python_update minimum_version maximum_version:
    # ensure git is clean
    git status | grep "nothing to commit" || exit 1

    just pin {{maximum_version}}
    just update_workflow {{minimum_version}} {{maximum_version}}

    # git add and commit

    git checkout -b 'update-python-{{maximum_version}}'

    git add .
    git commit -m "Update supported python to {{maximum_version}}, minimum version {{minimum_version}}"

    git push origin 'update-python-{{maximum_version}}'

    # create PR with gh
    gh pr create --title "Update supported python to {{maximum_version}}, minimum version {{minimum_version}}" --body "This PR updates the supported python version to {{maximum_version}}, with a minimum version of {{minimum_version}}"
