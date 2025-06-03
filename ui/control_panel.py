from infra.pubsub import PubSubClient
import gradio as gr
import subprocess
import json
import os
import time
import threading

# === Data Storage ===
commanders = {}
ninjas = {}
channel_map = {}

# === Ensure log directory exists ===
os.makedirs("log", exist_ok=True)

# === Commander Logic ===
def create_commander(name, strategy):
    if name in commanders:
        return f"⚠️ Commander '{name}' already exists."
    channel = f"{name}-channel"
    commanders[name] = {"strategy": strategy, "channel": channel}
    channel_map[name] = []

    try:
        logfile_path = os.path.join("log", f"commander_{name}.log")
        logfile = open(logfile_path, "w")
        subprocess.Popen(
            ["python", "nodes/commander_ai.py", "--name", name, "--channel", channel],
            stdout=logfile,
            stderr=logfile
        )
    except Exception as e:
        return f"❌ Failed to launch commander: {e}"

    return f"🧠 Commander '{name}' launched on channel '{channel}'"

def list_commanders():
    return json.dumps(commanders, indent=2)

# === Ninja Logic ===
def create_ninja(name, tools, assigned_commander):
    if name in ninjas:
        return f"Ninja '{name}' already exists."
    if assigned_commander not in commanders:
        return f"Commander '{assigned_commander}' not found."

    channel = commanders[assigned_commander]["channel"]
    ninjas[name] = {"tools": tools, "channel": channel}
    channel_map[assigned_commander].append(name)

    try:
        logfile_path = os.path.join("log", f"ninja_{name}.log")
        logfile = open(logfile_path, "w")
        subprocess.Popen(["python", "nodes/ninja.py", channel], stdout=logfile, stderr=logfile)
    except Exception as e:
        return f"❌ Failed to launch ninja: {e}"

    return f"🥷 Ninja '{name}' launched and subscribed to '{channel}'"

def list_ninjas():
    return json.dumps(ninjas, indent=2)

# === Logs ===
console_log_path = os.path.join("log", "console.log")

def read_console_log():
    if os.path.exists(console_log_path):
        with open(console_log_path, "r", encoding="utf-8") as f:
            return f.read()[-2000:]
    return "(No logs yet.)"

def start_auto_refresh(textbox):
    def loop():
        while True:
            time.sleep(3)
            textbox.value = read_console_log()
    threading.Thread(target=loop, daemon=True).start()

# === Docker Control ===
def start_nginx():
    try:
        subprocess.run(["docker", "run", "-d", "--name", "dummy-nginx", "-p", "8080:80", "nginx"], check=True)
        return "✅ Nginx started on port 8080"
    except subprocess.CalledProcessError:
        return "❌ Failed to start Nginx. Is Docker running?"

def stop_nginx():
    try:
        subprocess.run(["docker", "rm", "-f", "dummy-nginx"], check=True)
        return "🛑 Nginx container stopped"
    except subprocess.CalledProcessError:
        return "❌ Failed to stop Nginx container"

# === Publish Manual Attack ===
def publish_attack_cmd(cmd, channel_name):
    if not cmd.strip():
        return "⚠️ Empty command"
    try:
        pub = PubSubClient(channel=channel_name)
        pub.publish(cmd.strip())
        return f"✅ Sent '{cmd}' to '{channel_name}'"
    except Exception as e:
        return f"❌ Failed to send command: {e}"

# === Utility ===
def get_channel_map():
    return json.dumps(channel_map, indent=2)

# === UI ===
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 LLM-DDOS Simulation UI\nLaunch Commander AI, deploy Ninja nodes, and simulate attacks.")

    # === Commander Setup ===
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1️⃣ Launch Commander")
            commander_name = gr.Text(label="Commander Name")
            commander_strategy = gr.Text(label="Strategy")
            create_commander_btn = gr.Button("Launch Commander")
            commander_output = gr.Textbox(label="Output")
            create_commander_btn.click(create_commander, [commander_name, commander_strategy], commander_output)

        with gr.Column():
            gr.Markdown("### 📋 Commander Configs")
            list_commanders_btn = gr.Button("List Commanders")
            commanders_list = gr.Textbox(label="Commanders", lines=10)
            list_commanders_btn.click(list_commanders, outputs=commanders_list)

    # === Ninja Setup ===
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 2️⃣ Launch Ninja")
            ninja_name = gr.Text(label="Ninja Name")
            ninja_tools = gr.Text(label="Tools")
            ninja_commander = gr.Text(label="Assign to Commander")
            create_ninja_btn = gr.Button("Launch Ninja")
            ninja_output = gr.Textbox(label="Output")
            create_ninja_btn.click(create_ninja, [ninja_name, ninja_tools, ninja_commander], ninja_output)

        with gr.Column():
            gr.Markdown("### 📋 Ninja Configs")
            list_ninjas_btn = gr.Button("List Ninjas")
            ninjas_list = gr.Textbox(label="Ninjas", lines=10)
            list_ninjas_btn.click(list_ninjas, outputs=ninjas_list)

    # === Docker Target ===
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🐳 Target Nginx Server")
            start_btn = gr.Button("Start Nginx")
            stop_btn = gr.Button("Stop Nginx")
            docker_output = gr.Textbox(label="Status")
            start_btn.click(start_nginx, outputs=docker_output)
            stop_btn.click(stop_nginx, outputs=docker_output)

        with gr.Column():
            gr.Markdown("### 🔗 Channel Mapping")
            channel_mapping_output = gr.Textbox(label="Mappings", lines=10)
            list_mapping_btn = gr.Button("Show Mapping")
            list_mapping_btn.click(get_channel_map, outputs=channel_mapping_output)

    # === Manual Trigger ===
    with gr.Row():
        gr.Markdown("💥 Manual Attack Command")
        manual_cmd = gr.Textbox(label="Command (TCP, HTTP, SLOWLORIS)")
        target_channel = gr.Textbox(label="Channel Name", value="commander-1-channel")
        send_btn = gr.Button("Send Attack")
        manual_output = gr.Textbox(label="Send Status")
        send_btn.click(publish_attack_cmd, [manual_cmd, target_channel], manual_output)

    # === Logs ===
    with gr.Row():
        gr.Markdown("🖥️ Commander Console Log")
        log_display = gr.Textbox(label="Live Logs", lines=20)
        refresh_log_btn = gr.Button("🔄 Refresh Log")
        refresh_log_btn.click(fn=read_console_log, outputs=log_display)

if __name__ == "__main__":
    demo.launch(inbrowser=True)
