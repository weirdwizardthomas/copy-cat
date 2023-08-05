# Copy cat | one-way folder synchronisation

# Task

Implement a program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.

* Synchronization must be one-way: after the synchronization content of the
  replica folder should be modified to exactly match content of the source
  folder;
* Synchronization should be performed periodically.
* File creation/copying/removal operations should be logged to a file and to the
  console output;
* Folder paths, synchronization interval and log file path should be provided
  using the command line arguments;
* It is undesirable to use third-party libraries that implement folder
  synchronization;
* It is allowed (and recommended) to use external libraries implementing other
  well-known algorithms. For example, there is no point in implementing yet
  another function that calculates MD5 if you need it for the task – it is
  perfectly acceptable to use a third-party (or built-in) library.

# Running

1. Download Python (the project was developed with Python 3.11)
2. \[Optional\] Create virtual environment
3. Install requirements
   ```shell
    python -m pip install -r requirements.txt
   ```
4. Run `app.py`
   ```shell
   python app.py --source SOURCE-FOLDER --replica REPLICA-FOLDER --log LOG-FILE-PATH --interval INTERVAL [ms]

```
