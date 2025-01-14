# Zuri
Zuri verifies GitHub repositories for legitimacy and code quality, and monitors X accounts for tweet deletions and name changes.

![Zuribanner](https://github.com/user-attachments/assets/5b1cf19e-c3fb-4446-a583-d921fcee7699)

# Zuri - GitHub & X Account Verification Agent

Welcome to **Zuri**, an AI-powered agent designed to enhance the trustworthiness and quality assurance of open-source projects on GitHub and monitor changes in X accounts.

## Overview

Zuri is an innovative AI agent that:

- **Analyzes GitHub Repositories** for legitimacy, quality, and error-free code.
- **Monitors X Accounts** for changes in content or identity, such as deleted tweets or name changes.

## Features

### GitHub Repository Verification

- **Legitimacy Check**: Ensures that the repository is not a clone or contains plagiarized content.
- **Code Quality Assessment**: Scans for errors, style adherence, and potential security vulnerabilities.
- **Errorless Code Verification**: Uses advanced algorithms to check if the code is free from syntax errors or logical mistakes.

### X Account Monitoring

- **Tweet History**: Checks if any tweets have been deleted from the account.
- **Account Identity**: Monitors if the account has changed its display name or username.

## Usage

### GitHub Repository Analysis

1. **Input Repository URL**: Provide the URL of the GitHub repository you want to analyze.
2. **Run Zuri**: Execute the command:

   ```bash
   zuri analyze-repo <(https://github.com/agentzuri/Zuri)>

Review Results: Zuri will return a detailed report on the legitimacy and quality of the code.

X Account Monitoring
Input X Account: Specify the X account you want to monitor, e.g., x.com/agent_zuri.
Run Zuri: Use the following command:
bash
zuri monitor-account <x-account-url>
Check for Updates: Zuri will provide updates on any changes or deletions in the account's history.

Installation
To install Zuri, you need:

Python 3.8+
Git

Steps:

Clone the Repository:
bash
git clone https://github.com/agent_zuri/zuri.git
cd zuri
Install Dependencies:
bash
pip install -r requirements.txt
Configure Zuri:
Set up your GitHub and X API keys in a .env file or through environment variables.

Configuration
You will need to:

Add your GitHub API token in config.json or as an environment variable.
Add your X API credentials similarly.

json
{
  "github_api_token": "893hiuabneiu3",
  "x_api_key": "J9K4m6P2a8Z1d7X3n0E5W8b7L2G1f4Y",
  "x_api_secret": "T3S7z2B8g5K1M4e6N0V7l9C2D8q3F1A"
}

Contributing
We welcome contributions! Here's how you can help:

Report Bugs: Use GitHub Issues to report any bugs or issues you encounter.
Suggest Features: Propose new features or enhancements.
Contribute Code: Fork the repository, make your changes, and submit a pull request.

License
Zuri is released under the MIT License (LICENSE).

Contact
For any questions or further information, please contact us at:

X: 
x.com/agent_zuri
Email: support@zuri.ai

Feel free to join the discussion or ask questions in our GitHub repository's issues section.

Acknowledgements
Thanks to the open-source community for the fantastic tools and libraries that Zuri leverages.
Special thanks to our contributors for their invaluable feedback and code contributions.

Happy verifying with Zuri!
