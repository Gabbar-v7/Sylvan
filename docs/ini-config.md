# Configuration File

This file defines general settings for the **Sylvan Backend**.

## `config.ini` Variable

Create a file named config.ini in the project root and add the following variables:

```ini
[application]
env_file = env.development
enable_traceback = true

[database]
echo = false
max_overflow = 10
pool_timeout = 30
```

**Note:** This file contains Configurations that can be modified as per requirement.
