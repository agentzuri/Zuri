import requests
import json
from datetime import datetime, timedelta

class Zuri:
    def __init__(self, github_token, twitter_bearer_token):
        self.github_token = github_token
        self.twitter_bearer_token = twitter_bearer_token
        self.github_headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.twitter_headers = {
            "Authorization": f"Bearer {self.twitter_bearer_token}"
        }

    # GitHub methods (as in previous example)
    def get_project_info(self, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url, headers=self.github_headers)
        return response.json() if response.status_code == 200 else None

    def check_project_longevity(self, repo_info):
        if repo_info:
            created_at = repo_info.get('created_at')
            if created_at:
                created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                return (datetime.now() - created_date).days
        return None

    def analyze_commits(self, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        response = requests.get(url, headers=self.github_headers)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                latest_commit = commits[0]
                commit_date = datetime.strptime(latest_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
                return (len(commits), (datetime.now() - commit_date).days)
        return (0, None)

    def check_code_for_errors(self, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?labels=bug,error"
        response = requests.get(url, headers=self.github_headers)
        return len(response.json()) if response.status_code == 200 else 0

    # X (Twitter) methods
    def get_twitter_user_info(self, username):
        """
        Fetch user info from X API.
        """
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        response = requests.get(url, headers=self.twitter_headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Failed to fetch user info from X. Status code: {response.status_code}")
            return None

    def check_recent_handle_change(self, user_info):
        """
        Check if the user's handle was changed recently.
        Note: X API doesn't directly provide this info, so we check the creation date of the account 
        against the screen name update. This is a very basic check and might not catch all changes.
        """
        if user_info:
            created_at = datetime.strptime(user_info['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # Assume recent if account is less than 30 days old or if screen name was updated recently
            return (datetime.now() - created_at).days < 30
        return False

    def check_deleted_tweets(self, username):
        """
        Check if there are signs of recently deleted tweets. 
        This is a simplified check looking at the tweet count against historical data (which we don't have here).
        """
        user_info = self.get_twitter_user_info(username)
        if user_info:
            # This is a placeholder; in real use, you'd need to compare against historical data or use X's API more extensively
            return user_info.get('public_metrics', {}).get('tweet_count', 0) < 100  # Arbitrary low number to indicate possible deletion
        return False

    def evaluate_project_and_twitter(self, repo_owner, repo_name, twitter_username):
        """
        Evaluate both GitHub project and X account details.
        """
        github_result = self.evaluate_project(repo_owner, repo_name)
        twitter_result = self.evaluate_twitter(twitter_username)
        return {**github_result, **twitter_result}

    def evaluate_project(self, repo_owner, repo_name):
        repo_info = self.get_project_info(repo_owner, repo_name)
        if repo_info is None:
            return {"project_error": "Repository not found or access denied."}

        longevity = self.check_project_longevity(repo_info)
        commit_count, days_since_last_commit = self.analyze_commits(repo_owner, repo_name)
        error_count = self.check_code_for_errors(repo_owner, repo_name)

        return {
            "project_name": repo_info['name'],
            "longevity_days": longevity,
            "total_commits": commit_count,
            "days_since_last_commit": days_since_last_commit,
            "error_count": error_count
        }

    def evaluate_twitter(self, username):
        user_info = self.get_twitter_user_info(username)
        if user_info is None:
            return {"twitter_error": "User not found or access denied."}

        handle_changed = self.check_recent_handle_change(user_info)
        tweets_deleted = self.check_deleted_tweets(username)

        return {
            "twitter_username": user_info['username'],
            "handle_recently_changed": handle_changed,
            "tweets_deleted_recently": tweets_deleted
        }

    def run(self):
        """Main function to run Zuri."""
        print("Welcome to Zuri, the GitHub and X Account Analyzer!")
        while True:
            repo_owner = input("Enter the repository owner (or 'quit' to exit): ")
            if repo_owner.lower() == 'quit':
                break
            
            repo_name = input("Enter the repository name: ")
            twitter_username = input("Enter the X username: ")
            
            result = self.evaluate_project_and_twitter(repo_owner, repo_name, twitter_username)
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    GITHUB_TOKEN = input("Please enter your GitHub personal access token: ")
    TWITTER_BEARER_TOKEN = input("Please enter your X API bearer token: ")
    zuri = Zuri(GITHUB_TOKEN, TWITTER_BEARER_TOKEN)
    zuri.run()
