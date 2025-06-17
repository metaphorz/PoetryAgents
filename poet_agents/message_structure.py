"""Example message structure used by PoetryAgent send/receive functions."""

# A message is a dictionary with keys:
#   sender_id: str
#   recipient_id: str
#   message_type: str (e.g., 'poem')
#   payload: str (poem text)
#   timestamp: float (Unix time)

example_message = {
    "sender_id": "alpha",
    "recipient_id": "beta",
    "message_type": "poem",
    "payload": "Some poem text...",
    "timestamp": 0.0,
}
