---
dg-publish: true
title: NaN
createTime: 2023-12-07 17:54
tags:
  - shell
---
## shell 命令popd和pushed

Here's a step-by-step guide on how to use `pushd` and `popd` commands:

1. **Using pushd:**
    
    - The `pushd` command is similar to `cd`, but it also saves the current directory onto a stack.
    - To use `pushd`, you can simply type `pushd` followed by the directory path you want to navigate to.
    - For example:
        
        `$ pushd /path/to/directory`
        
2. **Viewing the Stack:**
    
    - You can view the directory stack using the `dirs` command.
    - The stack is a collection of directories that you have recently visited using `pushd`.
    - To view the stack, you can type:
        
        `$ dirs -v`
        
3. **Navigating the Stack:**
    
    - Once you've built up a stack, you can use it as a collection of bookmarks or fast-travel waypoints.
    - You can move forward and backward in the stack using the `+N` and `-N` notation, where `N` is the index of the directory in the stack.
    - For example:
        
        `$ pushd +2   # Move forward in the stack by 2 $ pushd -1   # Move backward in the stack by 1`
        
4. **Using popd:**
    
    - The `popd` command is used to remove directories from the stack and return to the previous directory.
    - When you use `popd` without any arguments, it removes the first (zeroeth) item from the stack and makes the next item your current working directory.
    - For example:
        
        `$ popd       # Remove the first item from the stack and return to the previous directory`
        
5. **Clearing the Stack:**
    
    - You can clear the entire stack using the `dirs -c` command.
    - This will remove all directories from the stack.
    - For example:
        
        `$ dirs -c    # Clear the directory stack`
        

Overall, `pushd` and `popd` can be useful for managing multiple directories and navigating between them efficiently. They provide a way to save and return to specific directories, which can be helpful when working with complex directory structures.