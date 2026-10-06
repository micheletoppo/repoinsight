import os
import anthropic

class RepositoryAnalyzer:
    def __init__(self, api_key: str = None, workspace_id: str = None):
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        workspace_id = workspace_id or os.environ.get("ANTHROPIC_WORKSPACE_ID")
        
        headers = {}
        if workspace_id:
            headers["anthropic-workspace-id"] = workspace_id

        self.client = anthropic.Anthropic(
            api_key=api_key,
            default_headers=headers if headers else None
        )

    def analyze_repository(self, repo_name: str, code_data: dict) -> str:
        prompt_content = f"Analizza questo repository GitHub ({repo_name}):\n\n"
        for path, content in code_data.items():
            prompt_content += f"--- FILE: {path} ---\n{content}\n\n"

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system="Sei uno Senior Software Architect. Fornisci un'analisi dettagliata in formato Markdown: 1) Panoramica Architetturale, 2) Punti di Forza, 3) Vulnerabilità/Code Smells, 4) Consigli di Miglioramento.",
            messages=[
                {"role": "user", "content": prompt_content}
            ]
        )
        return response.content[0].text