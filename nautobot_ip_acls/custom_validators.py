"""Custom Validators."""

from nautobot.apps.models import CustomValidator


class RoleLowerCaseNameValidator(CustomValidator):
    """Company policy is that Role names must be lower-case."""

    model = "extras.role"

    def clean(self):
        """Role name validator."""
        role = self.context["object"]
        if role.name.lower() != role.name:
            self.validation_error({"name": "Names must be lower case only."})


class GitRepoValidator(CustomValidator):
    """Git Repo URL validator."""

    model = "extras.GitRepository"

    def clean(self):
        """Validate GitRepository Remote URL."""
        repo = self.context["object"]
        if "devops" not in repo.remote_url.lower():
            self.validation_error({"name": "Repo names should include 'devops'."})


custom_validators = [RoleLowerCaseNameValidator, GitRepoValidator]  # Important!
