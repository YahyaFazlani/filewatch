# Filewatch

A file organizer with a cli to add filetypes and choose a folder to put files of that type/extension into.

## Set up
1. Create a .env in the project directory

```shell
touch .env
```

2. Set a variable in the .env to your database location. As an example you can look at [.env.example](.env.example)

3. To install the cli to your computer and use it from anywhere, first **head to the project folder** run the following command for your OS:
    #### Windows
    ```shell
    pip install .
    ```

    #### Mac/Linux
    ```shell
    pip3 install .
    ```

## Commands
### Create
```shell
filewatch create FILETYPE FOLDER
```
Create a new filetype in the database with a specified folder for the filetype. All files which are of that filetype when filewatch is watching.

### Update
```shell
filewatch update FILETYPE NEW_FOLDER  [-m, --move]
```    
Update a filetype present in the database with a new folder. Option to move the files in the old folder to the new folder.

### Delete
```shell
filewatch delete FILETYPE [--df, --delete-folder]
```
Delete the filetype from the database. Option to delete the folder.

### Start
```shell
filewatch start [--path="."]
```
Start watching and move files accordingly. Option to change path to watch from, defaults to the current directory if not provided.
