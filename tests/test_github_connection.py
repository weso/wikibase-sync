import github

from rdfsync.githubcon.github_connection import update_github_repo, connect_to_github, connect_to_repository_github, \
    create_file_in_repo, create_pull_request_in_repo, create_new_branch
import pytest

# pushing the changes to github
github_token = "582891de87080dfb8b2d19fb15986077a2f66c28"
repository_name = "othub/GithubApiTest"
source_branch = "main"
target_branch = "test_branch"

file_name = "test_file_1.txt"
file_content = "this is a test"


def test_update_github_correct_first():
    # connecting
    g = connect_to_github(github_token)

    # getting the repo
    current_repository = connect_to_repository_github(g, repository_name)

    # creating the new branch branch
    create_new_branch(current_repository, source_branch, target_branch)

    # creating a new file in the newly added branch
    create_file_in_repo(current_repository,
                        file_name,  # file name
                        "adding file 2 from PyGithub",  # commit message
                        file_content,  # file content
                        target_branch)

    # creating a ppull request from newly added branch
    create_pull_request_in_repo(current_repository,
                                "test_github_pull",  # PR name
                                "working correctly",  # PR description
                                target_branch,
                                source_branch)

    # check pull requests and closing
    for pull in g.get_repo(repository_name).get_pulls('all'):
        if str(pull.title) == 'test_github_pull': #pull request title
            assert True
            pull.edit(state="closed")
            print('closing the pull request')

    # check new branch and deleting
    for branch in g.get_repo(repository_name).get_branches():
        if str(branch.name) == target_branch:
            assert True
            g.get_repo(repository_name).get_git_ref('heads/' + str(branch.name)).delete()
            print('deleting the branch')

def test_update_github_correct_second():
    update_github_repo(github_token=github_token, repository_name=repository_name, source_branch=source_branch,
                       target_branch=target_branch, file_name=file_name, file_content=file_content)

    g = connect_to_github(github_token)

    # check pull requests and closing
    for pull in g.get_repo(repository_name).get_pulls('all'):
        if str(pull.title) == 'Pull Request from RDFSYNC': #pull request title
            assert True
            pull.edit(state="closed")
            print('closing the pull request')

    # check new branch and deleting
    for branch in g.get_repo(repository_name).get_branches():
        if str(branch.name) == target_branch:
            assert True
            g.get_repo(repository_name).get_git_ref('heads/' + str(branch.name)).delete()
            print('deleting the branch')

