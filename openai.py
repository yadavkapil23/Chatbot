import requests
import os

api_key = "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"

url = "https://api.groq.com/openai/v1/chat/completions"  

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_bot_response(user_input):
    
    data = {
        "model": "gemma2-9b-it",  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
      
        bot_reply = response.json()["choices"][0]["message"]["content"]
        return bot_reply
    else:
    
        return f"Error: {response.status_code}, {response.text}"

def main():
    print("Chatbot is running! Type 'exit' to end the chat. : ")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye! See You Soon.")
            break

        bot_response = get_bot_response(user_input)
        print("AI : ", bot_response)

if __name__ == "__main__":
    main()
