from flask import Flask, request, render_template
import requests
import git
from io import BytesIO
from git import Repo

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form['username']
    repos = get_repos(username)
    analysis = []
    
    for repo in repos:
        analysis.append(analyze_repo(repo))
    
    return render_template('result.html', analysis=analysis, username=username)

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    repos = response.json()
    return repos

def analyze_repo(repo):
    # Clone the repository to memory
    repo_url = repo['clone_url']
    repo_name = repo['name']

    repo_analysis = {
        "repo_name": repo_name,
        "ai_generated": False,
        "analysis_details": []
    }
    
    try:
        # Clone the repo into a temporary directory in memory
        temp_repo = Repo.clone_from(repo_url, f"/tmp/{repo_name}")
        
        # Analyze the repo here (e.g., commit messages, code style, etc.)
        # This is a basic example and should be expanded with more detailed checks
        commits = list(temp_repo.iter_commits('master', max_count=10))
        for commit in commits:
            if "generated" in commit.message.lower() or "ai" in commit.message.lower():
                repo_analysis["ai_generated"] = True
                repo_analysis["analysis_details"].append("Suspicious commit message: " + commit.message)
        
    except Exception as e:
        repo_analysis["analysis_details"].append(f"Error analyzing repo: {str(e)}")
    
    return repo_analysis

if __name__ == '__main__':
    app.run(debug=True)
