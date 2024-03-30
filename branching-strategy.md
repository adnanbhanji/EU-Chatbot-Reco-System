# Branching Strategy

## Overview

Our branching strategy is designed to facilitate collaboration, maintain code quality, and streamline the development process. We primarily use feature branches to isolate changes and ensure that the `main` branch remains stable at all times.

## Main Branches

We have three main branches, each serving as the primary development branch for a specific model:

- `main`: Represents the production-ready state of our application.
- `gpt-bot`: Development branch for the GPT Bot model.
- `llama2-bot`: Development branch for the Llama2 Bot model.
- `custom-bot`: Development branch for the Custom Bot model.

## Feature Branches

Feature branches are short-lived branches created from the respective model branches to implement new features or address specific issues. These branches follow a naming convention that includes the model name followed by a descriptive feature name.

For example: `gpt-bot-whatsapp`

### Creating a Feature Branch

To create a new feature branch, follow these steps:

```bash
git checkout gpt-bot   # Checkout the appropriate model branch
git pull               # Pull the latest changes from the remote repository
git checkout -b gpt-bot-whatsapp   # Create a new feature branch
```

### Making Changes
Make your changes on the feature branch and commit them locally:

```bash
git add .
git commit -m "Implement WhatsApp integration for GPT Bot"
```

### Merging Changes
Once your changes are complete and tested, merge the feature branch into the model branch:

```bash
git checkout gpt-bot   # Checkout the appropriate model branch
git merge gpt-bot-whatsapp   # Merge the feature branch into the model branch
```

### Pull Requests
We use pull requests to review and merge changes into the main branches. All changes must be reviewed and approved before merging.

## Conclusion
By following this branching strategy, we aim to ensure that our codebase remains organized, stable, and conducive to collaborative development.
