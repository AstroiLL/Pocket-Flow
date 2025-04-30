from pocketflow import Node, Flow
from utils import call_llm
import sys

class ChatNode(Node):
    def prep(self, shared):
        # Initialize messages if this is the first run
        if "messages" not in shared:
            shared["messages"] = []
            print("Welcome to the chat! Type 'exit' to end the conversation.")
        
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            return None
        
        # Add user message to history
        shared["messages"].append({"role": "user", "content": user_input})
        
        # Return all messages for the LLM
        return shared["messages"]

    def exec(self, messages):
        if messages is None:
            return None
        
        # Call LLM with the entire conversation history
        response = call_llm(messages)
        return response
    
    def exec_fallback(self, prep_res, exc):
        error_message = str(exc)
        print(f"\nОшибка: {error_message}")
        if "API ключ не найден" in error_message or "No auth credentials found" in error_message:
            print("\nПожалуйста, настройте API ключ одним из способов:")
            print("1. Создайте файл .env в директории проекта со следующим содержимым:")
            print("   OPENROUTER_API_KEY=ваш_ключ_api")
            print("2. Или установите переменную окружения:")
            print("   export OPENROUTER_API_KEY=ваш_ключ_api")
        return "Извините, произошла ошибка при обработке запроса."

    def post(self, shared, prep_res, exec_res):
        if prep_res is None or exec_res is None:
            print("\nGoodbye!")
            return "exit"  # Изменено с None на "exit" для корректного перехода
        
        # Print the assistant's response
        print(f"\nAssistant: {exec_res}")
        
        # Add assistant message to history
        shared["messages"].append({"role": "assistant", "content": exec_res})
        
        # Loop back to continue the conversation
        return "continue"

class ExitNode(Node):
    """Терминальный узел для корректного завершения Flow"""
    def post(self, shared, prep_res, exec_res):
        # Ничего не делаем, просто завершаем Flow
        return "default"

# Create the flow with self-loop
chat_node = ChatNode()
exit_node = ExitNode()

chat_node - "continue" >> chat_node  # Loop back to continue conversation
chat_node - "exit" >> exit_node      # Handle exit action

flow = Flow(start=chat_node)

# Start the chat
if __name__ == "__main__":
    shared = {}
    flow.run(shared)
