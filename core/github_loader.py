import requests

def fetch_repo_files(repo_owner: str, repo_name: str, branch: str = "main") -> dict:
    """Recupera la struttura e il contenuto dei file da GitHub API."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Errore nel recupero del repository: status code {response.status_code}")

    data = response.json()
    files_content = {}

    # Estensioni valide da analizzare
    valid_extensions = ('.py', '.js', '.ts', '.go', '.md', '.json', '.html', '.css')

    for item in data.get('tree', []):
        path = item.get('path', '')
        if item.get('type') == 'blob' and path.endswith(valid_extensions):
            if not path.startswith(('venv/', 'node_modules/', '.git/')):
                file_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{path}"
                res = requests.get(file_url)
                if res.status_code == 200:
                    files_content[path] = res.text[:3000] # Limite per evitare prompt troppo lunghi

    return files_content