# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.29.1...HEAD)

### Added
### Changed
### Deprecated
### Removed
### Fixed

- Fixed error summary link for single checkboxes (`BooleanField`)
- Added missing default `headingLevel` on error summary components

### Security

## [0.29.1](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.29.0...v0.29.1) - 2025-11-27

### Changed

- Upgraded to [TNA Frontend `v0.29.1`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.29.1)

### Fixed

- Added missing `href` in back link component

## [0.29.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.28.0...v0.29.0) - 2025-11-27

### Changed

- Upgraded to [TNA Frontend `v0.29.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.29.0)

## [0.28.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.27.0...v0.28.0) - 2025-10-07

### Changed

- Upgraded to [TNA Frontend `v0.28.1`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.28.1)

## [0.27.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.26.0...v0.27.0) - 2025-10-07

### Added

- Allowed the details component to have a `caller()` function

### Changed

- Upgraded to [TNA Frontend `v0.27.1`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.27.1)

### Fixed

- Allowed `PastDate` and `FutureDate` validators to use `datetime` objects
- Date fields can use ISO 8601 dates as `data` in addition to the existing date formats
- Fixed issue with processing date fields using both `formdata` and `data`

## [0.26.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.25.0...v0.26.0) - 2025-10-07

### Changed

- Upgraded to [TNA Frontend `v0.26.1`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.26.1)
- Updated the error message when CSRF validation fails

### Fixed

- Fixed bug with non-persistence of date fields

## [0.25.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.24.0...v0.25.0) - 2025-09-15

### Changed

- Upgraded to [TNA Frontend `v0.25.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.25.0)
- `BooleanField` with `TnaCheckboxWidget` doesn't render a fieldset and takes the field `description` as the checkbox label

## [0.24.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.23.0...v0.24.0) - 2025-07-30

### Added

- Partial date fields (`TnaProgressiveDateField`, `TnaMonthField`, `TnaYearField`) can no be coersed to the end of the date range with `end_of_partial_date_range`
- New fieldset widget for optional use with `FormField`
- New UK postcode validator `UKPostcode`

### Changed

- Upgraded to [TNA Frontend `v0.24.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.24.0)
- Removed requirement for `deepmerge` package
- `include_today` parameter on `PastDate` and `FutureDate` validators changed to `include_now`

## [0.23.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.22.0...v0.23.0) - 2025-07-30

### Changed

- Upgraded to [TNA Frontend `v0.23.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.23.0)

## [0.22.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.21.0...v0.22.0) - 2025-07-21

### Added

- Added support for `FileField` and `MultipleFileField` from WTForms

### Changed

- Simplified CSRF error messages
- Upgraded to [TNA Frontend `v0.22.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.22.0)

## [0.21.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.20.1...v0.21.0) - 2025-06-30

### Added

- Added support for [WTForms widgets](https://wtforms.readthedocs.io/en/2.3.x/widgets/)

### Changed

- Upgraded to [TNA Frontend `v0.21.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.21.0)

## [0.20.1](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.20.0...v0.20.1) - 2025-06-13

### Changed

- Upgraded to [TNA Frontend `v0.20.1`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.20.1)

## [0.20.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.19.0...v0.20.0) - 2025-06-13

### Changed

- Upgraded to [TNA Frontend `v0.20.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.20.0)

## [0.19.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.18.0...v0.19.0) - 2025-06-11

### Changed

- Upgraded to [TNA Frontend `v0.19.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.19.0)

## [0.18.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.17.0...v0.18.0) - 2025-05-20

### Changed

- Upgraded to [TNA Frontend `v0.18.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.18.0)

## [0.17.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.16.0...v0.17.0) - 2025-04-22

### Changed

- Upgraded to [TNA Frontend `v0.17.0`](https://github.com/nationalarchives/tna-frontend/releases/tag/v0.17.0)

## [0.16.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.15.0...v0.16.0) - 2025-03-24

### Changed

- Upgraded TNA Frontend to `v0.16.0`

## [0.15.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.14.0...v0.15.0) - 2025-03-04

### Changed

- Upgraded TNA Frontend to `v0.15.0`

### Fixed

- Added missing form group classes and attributes for form components

## [0.14.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.13.0...v0.14.0) - 2025-02-28

### Changed

- Upgraded TNA Frontend to `v0.14.0`

## [0.13.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.12.0...v0.13.0) - 2025-02-19

### Changed

- Upgraded TNA Frontend to `v0.13.1`

## [0.12.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.11.0...v0.12.0) - 2025-02-10

### Changed

- Upgraded TNA Frontend to `v0.12.0`

## [0.11.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.10.0...v0.11.0) - 2025-01-28

### Changed

- Upgraded TNA Frontend to `v0.11.0`

## [0.10.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.9.0...v0.10.0) - 2025-01-27

### Changed

- Upgraded TNA Frontend to `v0.10.0`

## [0.9.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.8.1...v0.9.0) - 2025-01-27

### Changed

- Upgraded TNA Frontend to `v0.9.0`

## [0.8.1](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.8.0...v0.8.1) - 2025-01-21

### Changed

- Upgraded TNA Frontend to `v0.8.1`

### Fixed

- Fixed issue with incorrect global header markup

## [0.8.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.7.0...v0.8.0) - 2025-01-15

### Changed

- Upgraded TNA Frontend to `v0.8.0`

## [0.7.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.6.0...v0.7.0) - 2025-01-13

### Changed

- Upgraded TNA Frontend to `v0.7.0`

## [0.6.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.5.0...v0.6.0) - 2025-01-08

### Changed

- Upgraded TNA Frontend to `v0.6.0`

## [0.5.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.4.0...v0.5.0) - 2025-01-03

### Changed

- Upgraded TNA Frontend to `v0.5.0`

## [0.4.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.3.0...v0.4.0) - 2024-12-10

### Changed

- Upgraded TNA Frontend to `v0.4.0`

### Deprecated

- Removed the records list component

## [0.3.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.18...v0.3.0) - 2024-12-05

### Changed

- Upgraded TNA Frontend to `v0.3.0`

## [0.2.18](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.17...v0.2.18) - 2024-11-05

### Changed

- Upgraded TNA Frontend to `v0.2.18`

## [0.2.17](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.16...v0.2.17) - 2024-10-23

### Changed

- Upgraded TNA Frontend to `v0.2.17`

## [0.2.16](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.15...v0.2.16) - 2024-10-16

### Changed

- Upgraded TNA Frontend to `v0.2.16`

## [0.2.15](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.14...v0.2.15) - 2024-10-07

### Changed

- Upgraded TNA Frontend to `v0.2.15`

## [0.2.14](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.13...v0.2.14) - 2024-09-18

### Changed

- Upgraded TNA Frontend to `v0.2.14`

## [0.2.13](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.12...v0.2.13) - 2024-09-13

### Changed

- Upgraded TNA Frontend to `v0.2.13`

### Fixed

- Stopped pagination components breaking when no `items` are passed

## [0.2.12](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.11...v0.2.12) - 2024-09-05

### Changed

- Upgraded TNA Frontend to `v0.2.12`

## [0.2.11](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.10...v0.2.11) - 2024-08-30

### Changed

- Upgraded TNA Frontend to `v0.2.11`

## [0.2.10](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.9...v0.2.10) - 2024-08-30

### Changed

- Upgraded TNA Frontend to `v0.2.10`

## [0.2.9](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.8...v0.2.9) - 2024-08-21

### Changed

- Upgraded TNA Frontend to `v0.2.9`

## [0.2.8](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.7...v0.2.8) - 2024-08-16

### Changed

- Upgraded TNA Frontend to `v0.2.8`

### Fixed

- Fixed ignored `headingSize` for sidebar

## [0.2.7](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.6...v0.2.7) - 2024-08-12

### Changed

- Upgraded TNA Frontend to `v0.2.7`

## [0.2.6](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.5...v0.2.6) - 2024-08-02

### Changed

- Upgraded TNA Frontend to `v0.2.6`

## [0.2.5](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.4...v0.2.5) - 2024-07-30

### Changed

- Upgraded TNA Frontend to `v0.2.5`

## [0.2.4](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.3...v0.2.4) - 2024-07-30

### Changed

- Upgraded TNA Frontend to `v0.2.4`

## [0.2.3](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.2...v0.2.3) - 2024-07-30

### Changed

- Upgraded TNA Frontend to `v0.2.3`

## [0.2.2](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.1...v0.2.2) - 2024-07-24

### Changed

- Upgraded TNA Frontend to `v0.2.2`

## [0.2.1](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.2.0...v0.2.1) - 2024-07-19

### Changed

- Upgraded TNA Frontend to `v0.2.1`

## [0.2.0](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.34...v0.2.0) - 2024-07-15

### Changed

- Upgraded TNA Frontend to `v0.2.0`
- Renamed "files" component to "files list" (`files` -> `files-list`, `tnaFiles()` -> `tnaFilesList()`)
- Renamed "featured records" component to "records list" (`featured-records` -> `records-list`, `tnaFeaturedRecords()` -> `tnaRecordsList()`)
- Moved the grid component to utilities

### Removed

- Removed search filters component
- Removed sensitive image component

## [0.1.34](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.33...v0.1.34) - 2024-07-11

### Changed

- Upgraded TNA Frontend to `v0.1.65`

## [0.1.33](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.32...v0.1.33) - 2024-06-24

### Changed

- Upgraded TNA Frontend to `v0.1.62`

## [0.1.32](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.31...v0.1.32) - 2024-06-18

### Changed

- Upgraded TNA Frontend to `v0.1.60`

## [0.1.31](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.30...v0.1.31) - 2024-06-13

### Changed

- Upgraded TNA Frontend to `v0.1.59`

## [0.1.30](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.29...v0.1.30) - 2024-06-05

### Changed

- Upgraded TNA Frontend to `v0.1.58`

## [0.1.29](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.28...v0.1.29) - 2024-05-30

### Changed

- Upgraded TNA Frontend to `v0.1.57`

## [0.1.28](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.27...v0.1.28) - 2024-05-28

### Changed

- Upgraded TNA Frontend to `v0.1.56`

## [0.1.27](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.26...v0.1.27) - 2024-05-13

### Changed

- Upgraded TNA Frontend to `v0.1.54`

### Fixed

- Fixed issues with some templates, particularly around the theme selection

## [0.1.26](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.25...v0.1.26) - 2024-05-13

### Changed

- Upgraded TNA Frontend to `v0.1.53`

## [0.1.25](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.24...v0.1.25) - 2024-04-04

### Changed

- Upgraded TNA Frontend to `v0.1.51`

## [0.1.24](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.23...v0.1.24) - 2024-03-28

### Fixed

- Added missing SVG height attribute to global header icons

## [0.1.23](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.22...v0.1.23) - 2024-03-28

### Changed

- Upgraded TNA Frontend to `v0.1.50`
- Renamed "message" component to "warning"

## [0.1.22](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.21...v0.1.22) - 2024-03-27

### Fixed

- Card actions now work without attributes

## [0.1.21](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.20...v0.1.21) - 2024-03-26

### Changed

- Upgraded TNA Frontend to `v0.1.49`

## [0.1.20](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.19...v0.1.20) - 2024-03-25

### Changed

- Upgraded TNA Frontend to `v0.1.48`

## [0.1.19](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.18...v0.1.19) - 2024-03-19

### Changed

- Upgraded TNA Frontend to `v0.1.47`

## [0.1.18](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.17...v0.1.18) - 2024-03-14

### Changed

- Upgraded TNA Frontend to `v0.1.43`

### Fixed

- Base template now matches fixture of `layouts/_generic.njk` template from TNA Frontend

## [0.1.17](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.16...v0.1.17) - 2024-03-11

### Changed

- Upgraded TNA Frontend to `v0.1.43`

## [0.1.16](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.15...v0.1.16) - 2024-03-04

### Fixed

- Form element macros separated from main macros for support with `search-filters`

## [0.1.15](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.14...v0.1.15) - 2024-03-04

### Changed

- Upgraded TNA Frontend to `v0.1.42`

## [0.1.14](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.13...v0.1.14) - 2024-02-27

### Changed

- Upgraded TNA Frontend to `v0.1.40`

## [0.1.13](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.12...v0.1.13) - 2024-02-19

### Changed

- Upgraded TNA Frontend to `v0.1.39`

## [0.1.12](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.11...v0.1.12) - 2024-02-13

### Changed

- Upgraded TNA Frontend to `v0.1.38`

## [0.1.11](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.10...v0.1.11) - 2024-02-06

### Changed

- Upgraded TNA Frontend to `v0.1.36`
- Change the default `htmlLang` from `en-GB` to `en`

## [0.1.10](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.9...v0.1.10) - 2023-12-29

### Added

- Allow `htmlAttributes` on the base template
- Added new compound filters component

### Changed

- Upgraded TNA Frontend to `v0.1.34`

### Fixed

- Fixed attributes for lots of components
- Fixed `bodyAttributes` on the base template

## [0.1.9](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.8...v0.1.9) - 2023-12-29

### Changed

- Upgraded TNA Frontend to `v0.1.33`

## [0.1.8](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.7...v0.1.8) - 2023-12-14

### Fixed

- Fixed `bodyAttributes` in base template

## [0.1.7](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.6...v0.1.7) - 2023-12-14

### Changed

- Upgraded TNA Frontend to `v0.1.31`

## [0.1.6](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.5...v0.1.6) - 2023-12-01

### Changed

- Upgraded TNA Frontend to `v0.1.29-prerelease`

## [0.1.5](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.4...v0.1.5) - 2023-11-29

### Added

- Routes added for layout templates

### Changed

- Base template changed from `generic.html` to `base.html`

## [0.1.4](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.3...v0.1.4) - 2023-11-29

### Changed

- Refactor structure of project

## [0.1.3](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.2...v0.1.3) - 2023-11-29

### Changed

- Change package name back to `tna-frontend-jinja`
- Remove Poetry for dependency management

## [0.1.2](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.1...v0.1.2) - 2023-11-29

### Changed

- Change package name from `tna-frontend-jinja` to `tna_frontend_jinja`

## [0.1.1](https://github.com/nationalarchives/tna-frontend-jinja/compare/v0.1.0...v0.1.1) - 2023-11-28

### Changed

- Package structure updated

## 0.1.0 - 2023-11-28

Initial release made to PyPi
