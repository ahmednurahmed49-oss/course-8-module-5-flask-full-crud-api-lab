from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_id = max([event.id for event in events], default=0) + 1

    new_event = Event(new_id, data["title"])

    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Delete an event
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)