import sys
from dotenv import load_dotenv
from core.github_loader import fetch_repo_files
from core.claude_analyzer import RepositoryAnalyzer

load_dotenv()

def main():
    print("--- RepoInsight: GitHub Repository Analyzer ---")
    repo_input = input("Inserisci il repository da analizzare (es. psf/requests): ").strip()
    
    if "/" not in repo_input:
        print("Formato non valido! Usa la forma 'owner/repository'.")
        sys.exit(1)
        
    owner, repo = repo_input.split("/")
    
    try:
        print(f"\n1. Recupero file da GitHub ({repo_input})...")
        files = fetch_repo_files(owner, repo)
        print(f"   Trovati {len(files)} file rilevanti.")
        
        print("\n2. Invio a Claude API per l'analisi...")
        analyzer = RepositoryAnalyzer()
        report = analyzer.analyze_repository(repo_input, files)
        
        print("\n" + "="*50)
        print("REPORT GENERATO DA CLAUDE")
        print("="*50 + "\n")
        print(report)
        
    except Exception as e:
        print(f"\nErrore durante l'esecuzione: {e}")

if __name__ == "__main__":
    main()