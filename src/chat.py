# src/chat.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import load_rag_chain

def main():
    qa = load_rag_chain()
    print("=========================================")
    print(" 🩻 MediBot RAG System Ready!")
    print(" Type 'exit' or 'quit' to end session.")
    print("=========================================\n")

    while True:
        try:
            query = input("You: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            result = qa(query)
            print("\nBot:", result['result'])
            if result.get('source_documents'):
                print("\nSources:", ", ".join(result['source_documents']))
            print("\n" + "-"*50 + "\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()

