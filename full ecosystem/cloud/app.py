from flask import Flask, request
import openai, json, os, time

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def ask_gpt(prompt):
    context = "User memory:\n" + "\n".join(memory.values())

    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content

@app.route("/")
def home():
    return "JARVIS CLOUD ONLINE"

@app.route("/command")
def command():
    cmd = request.args.get("cmd")

    if "remember that" in cmd:
        fact = cmd.replace("remember that", "").strip()
        memory[str(time.time())] = fact
        save_memory()
        return "Memory saved"

    response = ask_gpt(cmd)
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)