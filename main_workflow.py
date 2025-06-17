import time
from poet_agents.poetry_agent import PoetryAgent
from poet_agents.style_guide import frederick_turner_style


def choose_form() -> str:
    forms = ["haiku", "blank verse", "sonnet", "villanelle", "general prose"]
    print("Choose a poetic form:")
    for idx, f in enumerate(forms, 1):
        print(f"{idx}. {f}")
    choice = int(input("Form number: "))
    return forms[choice - 1]


def main() -> None:
    theme = input("Theme for the conversation: ")
    poetic_form = choose_form()
    length = int(input("How many exchanges (2-5)? "))

    alpha = PoetryAgent("alpha", llm_model="o3")
    beta = PoetryAgent("beta", llm_model="o3")

    prompt = theme
    for i in range(length):
        poem_a = alpha.generate_poetry(prompt, frederick_turner_style, poetic_form)
        alpha.send_message("beta", "poem", poem_a)
        print(f"\n--- Alpha {i+1} ---\n{poem_a}\n")

        msg = beta.receive_message()
        if msg:
            prompt_b = beta.interpret_poetry(msg["payload"])
        else:
            prompt_b = theme
        poem_b = beta.generate_poetry(prompt_b, frederick_turner_style, poetic_form)
        beta.send_message("alpha", "poem", poem_b)
        print(f"--- Beta {i+1} ---\n{poem_b}\n")

        msg_a = alpha.receive_message()
        if msg_a:
            prompt = alpha.interpret_poetry(msg_a["payload"])
        time.sleep(0.2)


if __name__ == "__main__":
    main()
