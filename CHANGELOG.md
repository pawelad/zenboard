# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keepachangelog] and this project
adheres to [Semantic Versioning][semver].

## [Unreleased][unreleased]

## [v0.2.0][v0.2.0] - 2017-10-31
### Added
- Renamed `Board.name` field to `slug` and added proper `name` field.
- Added `Board.show_closed_pipeline` field.
- Added issue progress and available comments data to issue card.
  Note: huge performance drop when fetching a 'fresh' board.
- Added `pipelines` URL field to `BoardSerializer`.

### Changed
- Created `Issue` helper class and moved `get_issue_details` function there.
- Minor frontend changes to Django REST Framework views.
- Major frontend changes.
- Don't require `GITHUB_API_TOKEN` and `ZENHUB_API_TOKEN` to be set and log a
  warning message if they're not.

### Fixed
- `Board.filter_sign` can be left blank.

## [v0.1.1][v0.1.1] - 2017-10-28
### Fixed
- Fixed superusers being able to see all boards (as intended), but not be able
  to see board issues details. ([#1])
- Fixed `Closed` pipeline always being empty. ([#2])

## [v0.1.0][v0.1.0] - 2017-10-23
### Added
- Initial release.


[keepachangelog]: http://keepachangelog.com/en/1.0.0/
[semver]: http://semver.org/spec/v2.0.0.html

[unreleased]: https://github.com/pawelad/zenboard/compare/v0.2.0...HEAD
[v0.1.0]: https://github.com/pawelad/zenboard/releases/tag/v0.1.0
[v0.1.1]: https://github.com/pawelad/zenboard/releases/tag/v0.1.1
[v0.2.0]: https://github.com/pawelad/zenboard/releases/tag/v0.2.0

[#1]: https://github.com/pawelad/zenboard/issues/1
[#2]: https://github.com/pawelad/zenboard/issues/2
