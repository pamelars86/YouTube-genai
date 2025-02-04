# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-02-04
### Added
- Added a new endpoint: `/slack_post/<video_id>`, allowing users to generate Slack posts from video content.

### Changed
- Renamed parameters in `prompt.yaml` to allow customization of prompts for Slack posts.

## [1.0.1] - 2025-02-02

### Added
- Added support for using OpenAI or models available in Ollama. Users can choose whether to use OpenAI, but they need to check the `README.md` file for OpenAI configuration.
- Reorganized the endpoint structure. Now, there is only one endpoint: `/blog_post/<video_id>`, simplifying API interactions.

### Changed
- The blog post generation system now uses a separate `prompt.yaml` file to store prompts instead of embedding them in the code. This makes it easier to manage and modify prompts.

## [0.0.1] - 2025-01-28
### Added
- Initial version of the API with two endpoints.
- The application only allowed Ollama models for generating blog posts.