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
  - [ ] Commit version bump in `pyproject.toml`
    - [ ] Commit message must be `Prepare v<new_version> release` (e.g. `Prepare v1.0.0 release`)
  - [ ] Tag commit with new release number
    - [ ] Tag name must be v-prefixed, followed by the semantic version (e.g.
      `v1.0.0`)
  - [ ] Push new commit and tag with `git push && git push --tags`
- [ ] Post-Release
  - [ ] Check [package page on PyPI](https://pypi.org/project/automython/) to
    ensure that new release is public
  - [ ] Post new GitHub Release with release notes