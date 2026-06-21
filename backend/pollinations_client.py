from pollinations import Pollinations

def ask_pollinations(prompt: str, history: list = None):
    try:
        client = Pollinations()
        
        messages = []
        if history:
            for msg in history:
                role = "assistant" if msg["role"] in ["assistant", "model"] else "user"
                messages.append({"role": role, "content": msg["content"]})
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            messages=messages,
            model="openai",
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f" Ошибка Pollinations: {str(e)}"