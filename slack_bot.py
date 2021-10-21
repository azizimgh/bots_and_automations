

token ="xoxb-2505109022784-2481519728210-h2g1WHU5BjYQv7J0YX1qhS2Q"
from slack import WebClient
slack_client = WebClient(token)

try:
  response = slack_client.chat_postMessage(
    channel="C02EJ3WLG1X",
    text="Hello from your app! :tada:"
  )
except Exception as e:
  # You will get a SlackApiError if "ok" is False
  print( e)


