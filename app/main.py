import os
from dotenv import load_dotenv

from .agent import SupportAgent


def main():

    load_dotenv()

    agent = SupportAgent()

    print()
    print("=" * 50)
    print("ASTER & ROW SUPPORT AGENT")
    print("=" * 50)
    print("Type 'exit' to quit.")
    print()

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":
            break

        try:
            answer = agent.answer(question)

            print()
            print("Agent:", answer)
            print()

        except Exception as e:
            print()
            print("ERROR:", e)
            print()


if __name__ == "__main__":
    main()