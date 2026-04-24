# Keep a Changelog

Our changelog rules generally follow [keepachangelog.com](https://keepachangelog.com/en/1.1.0/).

This project keeps the changelog in `.yaml` files within the `changelog` directory. The `!unreleased.yaml` file contains changes that are merged into main but have not been part of a stable release yet. 
::: info
This is the file that is modified as part of the pull request process. 
:::
::: warning
`CHANGELOG.md` as well as `{VERSION}.yaml` files are auto generated as part of the release process and should not be manually modified.
:::

Each changelog entry should be added to the `changes:` array in the `!unreleased.yaml` file where each entry has the follwing structure:

```yaml
# This can be either `fix`, `add`, `change`, `remove`, or an arbitrary string although in that case it will always be ordered last.
# Pick one
- type: "fix | add | change | remove"
    # List of projects that were affected by the given change. When picking what projects to choose dependencies should be considered,
    # meaning a pull request introducing changes in e.g. `Core` should also contain the packages `App` and `CLI` as they depend on `Core`.
    # Pick as many as apply.
    packages: ["App", "CLI", "Core", "Common", "ModKit", "RED4"]
    # Pull request number associated with this change.
    pr-number: 0
    # Authors github username, necessary for proper attribution
    author: ""
    # User facing change description
    description: ""
```


