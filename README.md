# Autonomous Executive Assistant Environment

## Overview
This environment simulates a real-world executive assistant task where an AI agent:
- manages emails
- extracts actionable tasks
- prioritizes work
- schedules meetings
- sends professional replies

## Motivation
Email overload is a real productivity bottleneck. This environment enables training and evaluating AI agents for real-world office automation.

## Observation Space
- Emails (id, sender, subject, body, processed, label)
- Tasks (description, priority, deadline)
- Calendar events (time, location)

## Action Space
Agent can:
- classify_email
- extract_task
- schedule_event
- send_reply
- mark_spam

Each action includes structured fields like email_id, description, time, etc.

## Tasks
- Easy: Email classification
- Medium: Classification + task extraction
- Hard: Full workflow (classification, scheduling, replies)

## Reward Design
- Positive rewards for correct actions
- Negative rewards for incorrect or invalid actions
- Encourages correct sequencing of actions

## Setup

```bash
pip install -r requirements.txt
python inference.py