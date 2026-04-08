from env import ExecutiveAssistantEnv
from models import Action


# -------------------------
# RULE-BASED AGENT
# -------------------------

def simple_agent(observation):

    # If there are unprocessed emails
    for email in observation["emails"]:

        # Skip already processed
        if email["processed"]:
            continue

        email_id = email["id"]
        text = (email["subject"] + " " + email["body"]).lower()

        # 1. Spam detection
        if "sale" in text or "offer" in text or "discount" in text:
            return Action(
                action_type="mark_spam",
                email_id=email_id
            )

        # 2. Classification
        if "submit" in text or "report" in text:
            return Action(
                action_type="classify_email",
                email_id=email_id,
                label="actionable"
            )

        if "meet" in text or "sync" in text:
            return Action(
                action_type="classify_email",
                email_id=email_id,
                label="actionable"
            )

        # Default classification
        return Action(
            action_type="classify_email",
            email_id=email_id,
            label="informational"
        )

    # 3. Extract tasks if any email classified
    for email in observation["emails"]:
        if email["label"] in ["actionable", "urgent"]:
            return Action(
                action_type="extract_task",
                email_id=email["id"],
                description=email["subject"]
            )

    # 4. Schedule event if any task exists
    if observation["tasks"]:
        task = observation["tasks"][0]
        return Action(
            action_type="schedule_event",
            task_id=task["id"],
            time="Tuesday 2 PM",
            location="Blue Room"
        )

    # 5. Reply if needed
    for email in observation["emails"]:
        if email["label"] == "actionable":
            return Action(
                action_type="send_reply",
                email_id=email["id"],
                message="Acknowledged."
            )

    return Action(action_type="invalid")


# -------------------------
# RUN ONE TASK
# -------------------------

def run_task(difficulty):

    env = ExecutiveAssistantEnv(difficulty=difficulty)
    obs = env.reset()

    total_reward = 0
    done = False

    while not done:
        obs_dict = obs.model_dump()

        action = simple_agent(obs_dict)

        obs, reward, done, _ = env.step(action)
        total_reward += reward

    max_possible = 5
    normalized_score = max(0.0, min(1.0, total_reward / max_possible))

    return normalized_score


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":

    print("Running rule-based inference...")

    results = {}

    for difficulty in ["easy", "medium", "hard"]:
        score = run_task(difficulty)
        print(f"{difficulty} score: {score}")
        results[difficulty] = score

    print("\nFinal Results:")
    print(results)