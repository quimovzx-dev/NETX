from config import APP_NAME, VERSION
from database.db import create_tables, history, stats
from core.engine import run

def banner():
    print(r"""\n╔══════════════════════════════════════════╗
║        NETX — INTERNET INTELLIGENCE     ║
║                 ENGINE                   ║
╚══════════════════════════════════════════╝
""")
    print(f"{APP_NAME} v{VERSION}")
    print("Commands: /history  /stats  /help  /exit\n")

def show_help():
    print("""\nNETX commands:
  /history   Show recent research queries
  /stats     Show database statistics
  /help      Show commands
  /exit      Quit NETX
  Anything else is a research query.
""")

def main():
    create_tables()
    banner()
    while True:
        query = input("NETX > ").strip()
        if query.lower() in {"/exit", "exit", "quit", "q"}:
            print("NETX shutting down.")
            break
        if query.lower() == "/help":
            show_help()
            continue
        if query.lower() == "/history":
            rows = history()
            if not rows:
                print("No research history yet.\n")
            else:
                print("\nRecent research:")
                for q, count, created in rows:
                    print(f"  • {q} ({count} sources) — {created}")
                print()
            continue
        if query.lower() == "/stats":
            s = stats()
            print(f"\nSources stored: {s['sources']}")
            print(f"Queries stored: {s['queries']}")
            print(f"Unique URL hosts: {s['unique_hosts']}\n")
            continue
        if not query:
            continue
        try:
            results, json_path, html_path = run(query)
            print("\n========== TOP RESULTS ==========")
            for i, item in enumerate(results, 1):
                print(f"\n{i}. {item.get('title', 'Untitled')}")
                print(f"   Type: {item.get('source_type', 'web')}")
                print(f"   Score: {item.get('score', 0)}")
                print(f"   Summary: {item.get('summary', '')[:300]}")
                print(f"   URL: {item.get('url', '')}")
            print(f"\nJSON report: {json_path}")
            print(f"HTML report: {html_path}\n")
        except Exception as exc:
            print(f"\n[ERROR] {exc}\n")

if __name__ == "__main__":
    main()
