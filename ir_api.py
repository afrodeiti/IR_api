from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Repeater storage (not persistent — clears when server restarts)
active_intentions = []

def repeat_intention(intention_text, duration):
    """Simulate repeating an intention by printing it periodically."""
    start_time = time.time()
    while time.time() - start_time < duration:
        print(f"🔁 Repeating: {intention_text}")
        time.sleep(1)  # Adjust frequency here
    print(f"✅ Finished repeating: {intention_text}")

@app.route('/run-intention', methods=['POST'])
def run_intention():
    data = request.json
    intention = data.get("intention")
    duration = data.get("duration", 60)  # Default to 60 seconds

    if not intention:
        return jsonify({"success": False, "message": "No intention provided."}), 400

    # Start background repetition
    thread = threading.Thread(target=repeat_intention, args=(intention, duration))
    thread.start()

    # Log or track the intention if desired
    active_intentions.append({"intention": intention, "duration": duration})

    return jsonify({
        "success": True,
        "message": f"Intention is now running for {duration} seconds.",
        "intention": intention
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
