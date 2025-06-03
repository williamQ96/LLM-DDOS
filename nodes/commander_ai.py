import time
import requests
from infra.pubsub import PubSubClient
from llm.prompt_templates import SYSTEM_PROMPT
from infra.monitor import summarize_observation
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default='commander-1')
parser.add_argument('--channel', type=str, default='commander-1-channel')
args = parser.parse_args()

CHANNEL_NAME = args.channel
OLLAMA_MODEL = "mistral"
LOOP_INTERVAL_SEC = 10

pub = PubSubClient(channel=CHANNEL_NAME)
print(f"[COMMANDER AI] Connected to Redis channel: {CHANNEL_NAME}")

def get_observation():
    return summarize_observation()

def build_prompt(observation):
    return f"""{SYSTEM_PROMPT}

Observation:
{observation}

Decision:"""

def query_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        return data["response"].strip()
    except Exception as e:
        print(f"[COMMANDER AI] [!!] Ollama query failed: {e}")
        return ""

if __name__ == "__main__":
    print("================== Commander AI Node Started ==================")
    try:
        while True:
            obs = get_observation()
            prompt = build_prompt(obs)

            print(f"\n[COMMANDER AI] >>> Prompt to Ollama:\n{prompt}\n")

            result = query_ollama(prompt)
            decision_line = result.split("Decision:")[-1].strip().upper()
            valid_cmds = {"TCP", "HTTP", "SLOWLORIS"}

            if decision_line in valid_cmds:
                pub.publish(decision_line)
                print(f"[COMMANDER AI] [OK!] Published: {decision_line}")
            else:
                print(f"[COMMANDER AI] [NO!] Ignored output: '{decision_line}'")

            time.sleep(LOOP_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n[COMMANDER AI] Shutting down.")
