# Welcome to Verger 🌳

**Verger** is a lightweight, framework-agnostic tool that provides an interactive way to experiment with your AI **prompts**, **models**, and **tools** directly within your existing codebase.

By loading your resources directly from your Python modules, Verger ensures that your experimentation environment is identical to your development environment. This eliminates the need to maintain configurations in multiple places and avoids the error-prone process of copy-pasting code or API keys into external tools.

!!! quote "Stop copy-pasting. Stop secret-sharing. Embrace your code as the Single Source of Truth."

---

## 🛠️ Experiment where you Develop

Verger eliminates the friction between your code and your experimentation environment by providing a **Single Source of Truth** for your AI logic:

*   **🌱 No Dual Configuration**: Use your prompts, models, and tools exactly as they are defined in your project. No need to re-configure them for a playground.
*   **🔒 Secure & Local**: Verger reuses your local `.env` files and environment variables. Your API keys and secrets stay where they belong—on your machine.
*   **⚖️ Environment Consistency**: External playgrounds often use different versions or descriptions for tools (like a web-search tool) than your actual code. Verger ensures you experiment with your exact definitions and local libraries, so if it works in the playground, it works in your application.
*   **✨ Seamless Integration**: Automatically imports your definitions. Whether it's a simple string prompt or a complex agentic tool, Verger bridges them into an interactive interface.
*   **🪶 Minimalist**: A tiny footprint with minimal dependencies, focused entirely on streamlining your developer experience.

## ⚙️ How it Works

Verger dynamically imports your models, prompts, and tools directly from your Python modules. It provides a unified **Interactive Playground** where you can:

1.  **Select** any prompt or tool from your codebase.
2.  **Pick** the models you want to evaluate.
3.  **Experiment** in real-time and see immediate results side-by-side.

---

## 🚀 Key Features at a Glance

| Feature | Description |
| :--- | :--- |
| **Direct Loading** | Interacts with your Python objects directly—no proxies, no middle-men. |
| **Single Source of Truth** | Your code *is* the configuration. No more manual synchronization. |
| **Environment Parity** | Experiment and develop in the exact same execution environment. |
| **Framework Agnostic** | Supports LangChain, PydanticAI, and native functions out of the box. |
| **Interactive Interface** | A high-focus environment designed for rapid iteration. |

---

!!! tip "Ready to start experimenting?"
    Check out the [Quickstart Guide](quickstart.md) to get up and running in minutes! 🚀
