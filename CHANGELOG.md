# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-02-22
### Added
- Added support for using OpenAI or models available in Ollama. Users can choose whether to use OpenAI, but they need to check the `README.md` file for OpenAI configuration.
- Reorganized the endpoint structure. Now, there is only one endpoint: `/blog_post/<video_id>`, simplifying API interactions.

### Changed
- The blog post generation system now uses a separate `prompt.yaml` file to store prompts instead of embedding them in the code. This makes it easier to manage and modify prompts.

## [1.0.0] - 2025-01-28
### Added
- Initial version of the API with two endpoints.
- The application only allowed Ollama models for generating blog posts.