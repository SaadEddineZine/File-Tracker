We will use Python watchdog library for file tracking (cross platform).

 **First install the watchdog library using:**

`pip install watchdog`

When we use pip install it looks in the python packages online and imports the needed one:

[https://pypi.org](https://pypi.org/)

`import os`

**The os module** in Python provides a way of using operating system-dependent functionality. This includes interacting with the file system, such as creating, removing, and changing directories, as well as fetching environment variables. In this code, os is used to check for the existence of directories and files, create directories, and manipulate file paths.

**Package
Definition:** A package is a collection of related modules organized in a directory hierarchy. A package must contain a special file named __init__.py (which can be empty) to be recognized as a package by Python.

![image](https://github.com/user-attachments/assets/bbe2668a-0111-432d-90d6-ddcf97d58886)

![image](https://github.com/user-attachments/assets/aa34269d-e76a-4777-a65c-5c147e0b8045)

**Module
Definition:** A module is a single file (with a .py extension) that contains Python code. This code can include functions, classes, variables, and runnable code.

`import math_utils`

**Library
Definition:** A library is a collection of modules and packages that provide specific functionality. Libraries can be built-in (part of the Python standard library) or third-party (installed via package managers like pip). A library is a collection of modules and packages that provide specific functionality. Libraries can be built-in (part of the Python standard library) or third-party (installed via package managers like pip).

![image](https://github.com/user-attachments/assets/d21dd1e4-3bfd-4ec1-905e-cae196b0d851)

The module can be a built-in module then we just use import module without the package and from.

**The shutil module** offers a higher-level interface for file operations. It includes functions for copying and removing files and directories. In this code, shutil is specifically used to copy sensitive files from the monitored directory to a designated sensitive folder, ensuring that sensitive data is stored securely.

**The hashlib module** provides a way to create secure hash functions. It supports various hashing algorithms, including SHA-256, which is used in this code to compute the hash of files. This is important for verifying file integrity and ensuring that sensitive files have not been altered.

The syntax used for importing in Python does not inherently indicate whether the imported entity is a module, package, or part of a library. The from x import y syntax can be used for all three types, and without additional context or documentation, you cannot determine the nature of x or y just from the import statement alone.

Differences Between import x and from x import *
import x:
This statement imports the entire module x, but you must use the module name to access its contents.
Example:

`import math
result = math.sqrt(16)  # Accessing the sqrt function using the module name
`
Here, you can access any function or variable defined in the math module by prefixing it with math..
from x import *:
This statement imports all public functions, classes, and variables from the module x directly into the current namespace.
Example:

`from math import *
result = sqrt(16)  # Accessing the sqrt function directly without the module name`
In this case, you can use sqrt directly without needing to prefix it with math..

`from tkinter import *`
**The tkinter module** is the standard GUI toolkit for Python. By importing everything from tkinter, the code can create graphical user interface elements such as windows, buttons, labels, and text boxes. This code uses tkinter to create a user interface for monitoring file changes, allowing users to interact with the application.

`from watchdog.observers import Observer`
**The watchdog library** is used for monitoring file system events. The Observer class is responsible for watching a directory for changes, such as file creation, modification, or deletion. In this code, an Observer instance is created to monitor a specified directory for any changes.

`from watchdog.events import FileSystemEventHandler`
This import brings in the FileSystemEventHandler class, which is a base class for handling file system events. By subclassing this class, the code can define specific actions to take when files are modified or created. In this code, a custom event handler (FileChangeHandler) is created to log changes and alert the user if sensitive files are affected.

`import threading`
**The threading module** allows for the creation and management of threads in Python. This is useful for running tasks concurrently, such as monitoring file changes without freezing the GUI. In this code, threading is used to run the file monitoring process in a separate thread, ensuring that the user interface remains responsive while the application is actively monitoring the specified directory.

Hashing in computer science and coding refers to the process of converting input data (often called a "message") into a fixed-size string of characters, which is typically a sequence of numbers and letters. This output is known as a "hash value" or "hash code." Hashing is commonly used for various purposes, including:

Data Integrity: Hash functions can verify the integrity of data by producing a unique hash value for a given input. If the input data changes, even slightly, the hash value will change significantly, indicating that the data has been altered.
Password Storage: Instead of storing plain-text passwords, systems often store the hash of the password. When a user logs in, the system hashes the entered password and compares it to the stored hash. This way, even if the database is compromised, the actual passwords remain secure.
