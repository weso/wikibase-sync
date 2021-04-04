# modules and libs
import logging
from github import Github

# logger settings
logging.basicConfig()
logger = logging.getLogger("github")


class GithubConnection:

    @staticmethod
    def connect_to_github(token):
        """
        connects to github using token
        Parameters
        ----------
        token: your github access token

        Returns
        -------
        nothing, connects to github
        """
        try:
            gh = Github(token)
            logger.warning(msg="Successfully connected to Github")
            return gh
        except ConnectionError:
            logger.error(msg="Error while connecting to Github")

    @staticmethod
    def connect_to_repository_github(github, target_repo_name):
        """
        connects to a specified repository
        Parameters
        ----------
        github: github api connection
        target_repo_name: a repository name

        Returns
        -------
        the repository
        """
        try:
            repo = github.get_repo(target_repo_name)
            logger.warning(msg="Connected to the repository <" + target_repo_name + ">")
            return repo
        except ConnectionError:
            logger.error(msg="Error while connecting to a repository in Github")

    @staticmethod
    def create_new_branch(repo, base_branch, new_branch_name):
        """
        creates a new branch
        Parameters
        ----------
        repo: repository name
        base_branch: base branch
        new_branch_name: your new branch that will be created

        Returns
        -------
        updates the github repository with the new file

        """
        try:
            sb = repo.get_branch(base_branch)
            repo.create_git_ref(ref="refs/heads/" + new_branch_name, sha=sb.commit.sha)
            logger.warning(msg="New branch <" + new_branch_name + "> created successfully")
        except ConnectionError:
            logger.error(msg="Error while creating a branch in Github")

    @staticmethod
    def create_file_in_repo(repo, file_name, commit_msg, file_content, branch):
        """
        created a file in repository
        Parameters
        ----------
        repo: repo name
        file_name: filename
        commit_msg: commit message
        file_content: content of the file
        branch: the branch that will include the file created

        Returns
        -------
        updates the github repository with new file in a specified branch
        """
        try:
            repo.create_file(file_name, commit_msg, content=file_content, branch=branch)
            logger.warning(msg="A new file <" + file_name + "> created in <" + branch + ">")
        except ConnectionError:
            logger.error(msg="Error while creating a new file in Github")

    @staticmethod
    def create_pull_request_in_repo(repo, title, body, head, base):
        """

        Parameters
        ----------
        repo: repository name
        title: title of pr
        body: body of pr
        head: your base branch
        base: your branch name

        Returns
        -------
        created a pull request in a github repository
        """
        try:
            repo.create_pull(title=title, body=body, head=head, base=base)
            logger.warning("A pull request is successfully created in the repository <" + repo.name + ">")
        except ConnectionError:
            logger.error(msg="Error while creating a PR in Github")
    
    def update_github_repo(self, github_token: str, repository_name: str, source_branch: str, target_branch: str,
                           file_name: str,
                           file_content):
        """
        creates a pull request from the target branch with the resulting file

        Parameters
        ----------
        github_token: github token
        repository_name: name of the repository (username/repo_name)
        source_branch: your base branch
        target_branch: your new branch name
        file_name: the name of the file that will be created
        file_content: the resulting file content

        Returns
        -------
        updates the github repository with the created pull request.
        """
        # connecting
        g = self.connect_to_github(github_token)  # your github access token

        # getting the repo
        current_repository = self.connect_to_repository_github(g, repository_name)  # your repository name

        # creating the new branch branch
        self.create_new_branch(current_repository, source_branch, target_branch)

        # creating a new file in the newly added branch
        self.create_file_in_repo(current_repository,
                                 file_name=file_name,  # file name
                                 commit_msg="synchronization using rdfsync",  # commit message
                                 file_content=file_content,  # file content
                                 branch=target_branch)

        # creating a ppull request from newly added branch
        self.create_pull_request_in_repo(repo=current_repository,
                                         title="Pull Request from RDFSYNC",  # PR name
                                         body="Creating a pull request from " + target_branch + " to " + source_branch
                                              + " using RDFSYNC",  # PR description
                                         head=target_branch,
                                         base=source_branch)
