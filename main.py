from config import APP_NAME, VERSION
from database.db import create_tables
from core.engine import run

def banner():
    print(r"""
╔══════════════════════════════════════════╗
║        NETX — INTERNET INTELLIGENCE     ║
║                 ENGINE                   ║
╚══════════════════════════════════════════╝
""")
    print(f"{APP_NAME} v{VERSION}\n")

def main():
    create_tables()
    banner()
    while True:
        query = input("NETX > ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            print("NETX shutting down.")
            break
        if not query:
            continue
        try:
            results, json_path, html_path = run(query)
            print("\n========== TOP RESULTS ==========")
            for i, item in enumerate(results, 1):
                print(f"\n{i}. {item.get('title', 'Untitled')}")
                print(f"   Score: {item.get('score', 0)}")
                print(f"   URL: {item.get('url', '')}")
            print(f"\nJSON report: {json_path}")
            print(f"HTML report: {html_path}\n")
        except Exception as exc:
            print(f"\n[ERROR] {exc}\n")

if __name__ == "__main__":
    main()
