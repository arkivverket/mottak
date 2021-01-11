# Dependabot
We use dependabot to monitor dependency versions. To add a new application to dependabot monitoring, add it in
[dependabot.yaml](dependabot.yaml). For more documentation see
[dependabot documentation](https://docs.github.com/en/free-pro-team@latest/github/administering-a-repository/keeping-your-dependencies-updated-automatically).

# Building Github Actions workflows

### Adding new workflow
To create a new workflow you need to add a new service/component name to
[build-workflows.sh](build-worflows.sh) and run the script. This will then autogenerate
new workflows for all the services added to the script.

### Changing a workflow
Change the template file [python-workflow-template.yaml](python-workflow-template.yaml) and
run the bash script to generate new workflows.

### Adding support for new languages
Create a new template (use existing one for ideas), and add support for new templates
in [build-workflows.sh](build-worflows.sh)
