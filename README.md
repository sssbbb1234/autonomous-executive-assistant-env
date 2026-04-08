# Autonomous Executive Assistant Environment

## Description
This environment simulates a real-world executive assistant workflow:
- Email classification
- Task extraction
- Meeting scheduling
- Email response

## Tasks
- Easy: Spam classification
- Medium: Task extraction
- Hard: Scheduling + response

## Action Space
- classify_email
- extract_task
- schedule_event
- send_reply

## Observation Space
- Emails
- Tasks
- Calendar

## Running
python inference.py

## Output
Returns scores for each difficulty level (0–1)
