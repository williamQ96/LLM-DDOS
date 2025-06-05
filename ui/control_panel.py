from infra.pubsub import PubSubClient
import gradio as gr
import subprocess
import json

# --- Data ---
commanders = {}
ninjas = {}
channel_map = {}

# --- Commander Logic ---
def create_commander(name, strategy):
    if name in commanders:
        return f"Commander '{name}' already exists."
    commanders[name] = {"strategy": strategy, "channel": f"{name}-channel"}
    channel_map[name] = []
    return f"Commander '{name}' created with channel '{name}-channel'."

def list_commanders():
    return json.dumps(commanders, indent=2)

# --- Ninja Logic ---
def create_ninja(name, tools, assigned_commander):
    if name in ninjas:
        return f"Ninja '{name}' already exists."
    if assigned_commander not in commanders:
        return f"Commander '{assigned_commander}' not found."
    channel = commanders[assigned_commander]["channel"]
    ninjas[name] = {"tools": tools, "channel": channel}
    channel_map[assigned_commander].append(name)
    return f"Ninja '{name}' created and subscribed to '{channel}'."

def list_ninjas():
    return json.dumps(ninjas, indent=2)

# --- Docker Nginx Control ---
def start_nginx():
    try:
        subprocess.run(["docker", "run", "-d", "--name", "dummy-nginx", "-p", "8080:80", "nginx"], check=True)
        return "Nginx Docker container started on port 8080."
    except subprocess.CalledProcessError:
        return "Failed to start Nginx container. Is Docker running?"

def stop_nginx():
    try:
        subprocess.run(["docker", "rm", "-f", "dummy-nginx"], check=True)
        return "Nginx Docker container stopped."
    except subprocess.CalledProcessError:
        return "Failed to stop Nginx container."

# --- Redis Command Publish ---
def publish_attack_cmd(cmd):
    if not cmd.strip():
        return "⚠️ Empty command. Not sent."
    try:
        pub = PubSubClient()
        pub.publish(cmd.strip())
        return f"✅ Command '{cmd.strip()}' sent via Redis."
    except Exception as e:
        return f"❌ Failed to send command: {e}"

# === UI ===
with gr.Blocks() as demo:
    gr.Markdown("""# 🧠 LLM-DDOS Simulation UI
A prototype control panel to configure Commanders, Ninjas, and simulate attacks on a Docker-based Nginx target.""")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🧠 Configure Commanders")
            commander_name = gr.Text(label="Commander Name")
            commander_strategy = gr.Text(label="Strategy Description")
            create_commander_btn = gr.Button("Create Commander")
            commander_output = gr.Textbox(label="Output")
            list_commanders_btn = gr.Button("List All Commanders")
            commanders_list = gr.Textbox(label="Commander Configs")

            create_commander_btn.click(create_commander, [commander_name, commander_strategy], commander_output)
            list_commanders_btn.click(list_commanders, outputs=commanders_list)

        with gr.Column():
            gr.Markdown("### 🥷 Configure Ninjas")
            ninja_name = gr.Text(label="Ninja Name")
            ninja_tools = gr.Text(label="Tools (comma-separated)")
            ninja_commander = gr.Text(label="Assign to Commander")
            create_ninja_btn = gr.Button("Create Ninja")
            ninja_output = gr.Textbox(label="Output")
            list_ninjas_btn = gr.Button("List All Ninjas")
            ninjas_list = gr.Textbox(label="Ninja Configs")

            create_ninja_btn.click(create_ninja, [ninja_name, ninja_tools, ninja_commander], ninja_output)
            list_ninjas_btn.click(list_ninjas, outputs=ninjas_list)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🐳 Docker Control")
            start_btn = gr.Button("Start Nginx Server")
            stop_btn = gr.Button("Stop Nginx Server")
            docker_output = gr.Textbox(label="Docker Status")
            start_btn.click(start_nginx, outputs=docker_output)
            stop_btn.click(stop_nginx, outputs=docker_output)

        with gr.Column():
            gr.Markdown("### 🔗 Channel Mapping")
            channel_mapping_output = gr.Textbox(label="Commander ↔ Ninja Channels", interactive=False)
            list_mapping_btn = gr.Button("Show Channel Mapping")

            def get_channel_map():
                return json.dumps(channel_map, indent=2)

            list_mapping_btn.click(get_channel_map, outputs=channel_mapping_output)

    with gr.Group():
        gr.Markdown("💥 **Manual Attack Trigger**")
        manual_cmd_input = gr.Textbox(label="Attack Command", placeholder="e.g., TCP, HTTP, SLOWLORIS")
        send_btn = gr.Button("Send to Ninja")
        manual_output = gr.Textbox(label="Status")
        send_btn.click(fn=publish_attack_cmd, inputs=[manual_cmd_input], outputs=[manual_output])

if __name__ == "__main__":
    demo.launch(inbrowser=True)
