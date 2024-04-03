[//]: <https://github.com/caleb531/automata/blob/main/.github/RELEASE_CHECKLIST.md>
# Automython Release Checklist

If you are an Automata collaborator, this is a checklist you can follow to
properly publish a release to GitHub and PyPI.

- [ ] Before Release
  - [ ] Update README with latest major release (e.g. v8),
    if applicable
  - [ ] Write release notes for new release
  - [ ] Check copyright year (the end year in the range should always be the
    current year)
- [ ] Release
  - [ ] Change version to new version in `automython/interpret/cli.py`
  - [ ] Commit version bump with `$ bumpversion --current-version <new_version> <major/minor/patch>`
    - [ ] Commit message must be `Bump v<old_version> → <new_version>` (e.g. `Bump v1.0.0 → 1.0.1`)
  - [ ] Tag commit with new release number
    - [ ] Tag name must be v-prefixed, followed by the semantic version (e.g.
      `v1.0.0`)
  - [ ] Push new commit and tag with `git push && git push --tags`
- [ ] Post-Release
  - [ ] Check [package page on PyPI](https://pypi.org/project/automython/) to
    ensure that new release is public
  - [ ] Post new GitHub Release with release notes