import requests
import json
from datetime import datetime, timedelta

class Zuri:
    def __init__(self, github_token):
        self.github_token = github_token
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_project_info(self, repo_owner, repo_name):
        """
        Fetch basic information about the repository.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch repository info. Status code: {response.status_code}")
            return None

    def check_project_longevity(self, repo_info):
        """
        Check how long the project has been active.
        """
        if repo_info:
            created_at = repo_info.get('created_at')
            if created_at:
                created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                now = datetime.now()
                duration = now - created_date
                return duration.days
        return None

    def analyze_commits(self, repo_owner, repo_name):
        """
        Analyze the commit history to see if the project is actively maintained.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                latest_commit = commits[0]
                commit_date = datetime.strptime(latest_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
                return (len(commits), (datetime.now() - commit_date).days)
        return (0, None)

    def check_code_for_errors(self, repo_owner, repo_name):
        """
        A very simplified error check. In practice, you'd use static analysis tools like pylint or flake8.
        This method checks for open issues tagged as 'bug' or 'error'.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?labels=bug,error"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            issues = response.json()
            return len(issues)
        return 0

    def evaluate_project(self, repo_owner, repo_name):
        """
        Evaluate the legitimacy of a GitHub project.
        """
        repo_info = self.get_project_info(repo_owner, repo_name)
        if repo_info is None:
            return "Repository not found or access denied."

        longevity = self.check_project_longevity(repo_info)
        commit_count, days_since_last_commit = self.analyze_commits(repo_owner, repo_name)
        error_count = self.check_code_for_errors(repo_owner, repo_name)

        legitimacy_score = 0
        if longevity is not None:
            # Score based on longevity: up to 5 points
            legitimacy_score += min(longevity // 365, 5)  # 5 points for every full year up to 5 years

        # Score based on commit activity: up to 3 points
        if commit_count > 100:
            legitimacy_score += 3
        elif commit_count > 50:
            legitimacy_score += 2
        elif commit_count > 10:
            legitimacy_score += 1

        # Score based on recent activity: up to 2 points
        if days_since_last_commit is not None:
            if days_since_last_commit < 30:
                legitimacy_score += 2
            elif days_since_last_commit < 90:
                legitimacy_score += 1

        # Deduct points for errors (very simplified; real analysis would be much more complex)
        legitimacy_score -= min(error_count, 3)

        return {
            "project_name": repo_info['name'],
            "longevity_days": longevity,
            "total_commits": commit_count,
            "days_since_last_commit": days_since_last_commit,
            "error_count": error_count,
            "legitimacy_score": max(legitimacy_score, 0)  # Ensure score doesn't go negative
        }

    def run(self):
        """Main function to run Zuri."""
        print("Welcome to Zuri, the GitHub Project Legitimacy Checker!")
        while True:
            repo_owner = input("Enter the repository owner: ")
            repo_name = input("Enter the repository name: ")
            if repo_owner.lower() == 'quit' or repo_name.lower() == 'quit':
                print("Thank you for using Zuri. Goodbye!")
                break
            
            result = self.evaluate_project(repo_owner, repo_name)
            if isinstance(result, str):
                print(result)
            else:
                print(json.dumps(result, indent=2))

if __name__ == "__main__":
    GITHUB_TOKEN = input("Please enter your GitHub personal access token: ")
    zuri = Zuri(GITHUB_TOKEN)
    zuri.run()
