#!/usr/local/cs/bin/python3

import os
import sys
import zlib

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

def read_object(sha1, git_dir):
    object_path = os.path.join(git_dir, 'objects', sha1[0:2], sha1[2:])
    f = open(object_path, 'rb')
    content = zlib.decompress(f.read()).decode('utf-8')
    return content

def get_commit_list(branch_list, git_dir):
    commit_hashes = []
    for branch in branch_list:
        branch_commit_content = read_object(branch, git_dir)
        
        # Get the list of commit hashes in the branch
        
        current_commit = branch_commit_content.split('\n')[0].split(' ')[1]

        while current_commit not in commit_hashes:
            commit_hashes.append(current_commit)

            # Read the commit object
            commit_content = read_object(current_commit, git_dir)

            # Find the parent commit
            parent_line = next(line for line in commit_content.split('\n') if line.startswith('parent '))
            current_commit = parent_line.split(' ')[1]

    return commit_hashes

def get_branches_list(directory_path):          #problem 2
    print(directory_path)
    file_list = os.listdir(directory_path)
    print(file_list)
    result_branches = []
    for item in file_list:
        new_dir = directory_path + "/" + item
        if os.path.isdir(new_dir):
            result_branches.append(get_branches_list(new_dir))
        else:
            f = open(new_dir, 'r')
            head_ref = f.readline().strip()
            print(head_ref)
            result_branches.append(head_ref)
    return result_branches

def topo_order_commits():                                    #problem 1

    directory_path = os.getcwd()
    marker = False
    while(directory_path != '/'):
        file_list = os.listdir(directory_path)
        for i in file_list:
            if i == '.git':
                marker = True
                print("found")
                new_path2 = directory_path + "/.git/refs/heads"
                new_path3 = directory_path + "/.git"
                branch_list = get_branches_list(new_path2)             #problem 2
                get_commit_list(branch_list, new_path3)                          #problem 3
        directory_path = os.path.dirname(directory_path)

    if(marker == False):
        print("Not inside a Git repository.", file=sys.stderr) 


if __name__ == '__main__':
    topo_order_commits()
