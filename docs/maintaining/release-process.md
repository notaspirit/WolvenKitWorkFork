# Release Process

Stable releases are done by (or with the permission of) the project lead and are scheduled to be around the first every month.

Nightly releases get automatically build and released daily when changes on the `dev` branch are present.

## Before Releasing
Before releasing a new version via the release workflow the following things need to be ensured: 
1. Project version is correct for the type of release according to semver (if it isn't bump it via the github action)
2. All relevant change notes are staged in `changelog\!unreleased.yaml`

## Releasing 
To release for all platforms (Nuget Packages, Github, Nexusmods) simply manually trigger the release workflow. It will create a new tag, compile the changelog, build the assets and release them. 

## After Releasing 
1. Bump the patch version by one (e.g. if the stable release was `8.17.2` bump it to `8.17.3`) for the nightly builds. If at the time of the next stable release it is decided that it is not just a patch bump the version again then. 
2. Post the changelog from the github release in the `#updates` channel on the redmodding discord with links to all platforms and a ping to the `@Server-Participation` role.