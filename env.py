from models import Email, Task, CalendarEvent, Observation, Action
from tasks import ALL_TASKS
import uuid


class ExecutiveAssistantEnv:

    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.task_data = ALL_TASKS[difficulty]

        self.emails = []
        self.tasks = []
        self.calendar = []

        self.ground_truth = {}
        self.step_count = 0
        self.max_steps = 20

    def reset(self):
        self.step_count = 0

        self.emails = [
            Email(**email) for email in self.task_data["emails"]
        ]

        self.tasks = []
        self.calendar = []

        self.ground_truth = self.task_data["ground_truth"]

        return self._get_observation()

    def _get_observation(self):
        return Observation(
            emails=self.emails,
            tasks=self.tasks,
            calendar=self.calendar,
            step_count=self.step_count
        )

    def step(self, action: Action):

        reward = 0.0
        info = {}

        if action.action_type == "classify_email":
            reward += self._handle_classify(action)

        elif action.action_type == "extract_task":
            reward += self._handle_extract(action)

        elif action.action_type == "schedule_event":
            reward += self._handle_schedule(action)

        elif action.action_type == "send_reply":
            reward += self._handle_reply(action)

        elif action.action_type == "mark_spam":
            reward += self._handle_spam(action)

        else:
            reward -= 0.1  # invalid action

        # Update processed state
        self._update_processed()

        # Increment steps
        self.step_count += 1

        # Check done
        done = self._check_done()

        return self._get_observation(), reward, done, info


    def _handle_classify(self, action):
        email = self._find_email(action.email_id)
        if not email:
            return -0.2

        if email.processed:
            return -0.1

        email.label = action.label

        gt = self.ground_truth.get(email.id, {})
        if gt.get("label") == action.label:
            return 0.2
        else:
            return -0.2

    def _handle_extract(self, action):
        email = self._find_email(action.email_id)
        if not email:
            return -0.2

        if email.label not in ["actionable", "urgent"]:
            return -0.2

        # Prevent duplicate task
        for t in self.tasks:
            if t.source_email_id == email.id:
                return -0.1

        task_id = str(uuid.uuid4())

        new_task = Task(
            id=task_id,
            description=action.description,
            source_email_id=email.id
        )

        self.tasks.append(new_task)

        gt = self.ground_truth.get(email.id, {})
        if gt.get("task") and gt["task"].lower() in action.description.lower():
            return 0.3
        else:
            return -0.2

    def _handle_schedule(self, action):
        task = self._find_task(action.task_id)
        if not task:
            return -0.2

        # Prevent duplicate scheduling
        for e in self.calendar:
            if e.linked_task_id == task.id:
                return -0.1

        event = CalendarEvent(
            event_id=str(uuid.uuid4()),
            title=task.description,
            time=action.time,
            location=action.location,
            linked_task_id=task.id
        )

        self.calendar.append(event)

        gt = self.ground_truth.get(task.source_email_id, {})
        if gt.get("time") == action.time:
            return 0.3
        else:
            return -0.2

    def _handle_reply(self, action):
        email = self._find_email(action.email_id)
        if not email:
            return -0.2

        email.replied = True

        gt = self.ground_truth.get(email.id, {})
        if gt.get("reply_required"):
            return 0.2
        else:
            return -0.1

    def _handle_spam(self, action):
        email = self._find_email(action.email_id)
        if not email:
            return -0.2

        email.label = "spam"

        gt = self.ground_truth.get(email.id, {})
        if gt.get("label") == "spam":
            return 0.2
        else:
            return -0.2


    def _find_email(self, email_id):
        for e in self.emails:
            if e.id == email_id:
                return e
        return None

    def _find_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def _update_processed(self):
        for email in self.emails:
            gt = self.ground_truth.get(email.id, {})

            if not email.label:
                continue

            # Spam → done
            if gt.get("label") == "spam":
                email.processed = True
                continue

            # Task check
            task_done = True
            if "task" in gt:
                task_done = any(t.source_email_id == email.id for t in self.tasks)

            # Schedule check
            schedule_done = True
            if "time" in gt:
                schedule_done = any(
                    e.linked_task_id == t.id
                    for t in self.tasks if t.source_email_id == email.id
                    for e in self.calendar
                )

            # Reply check
            reply_done = True
            if gt.get("reply_required"):
                reply_done = email.replied

            if task_done and schedule_done and reply_done:
                email.processed = True

    def _check_done(self):
        all_processed = all(e.processed for e in self.emails)
        return all_processed or self.step_count >= self.max_steps

    def state(self):
        return {
            "emails": self.emails,
            "tasks": self.tasks,
            "calendar": self.calendar,
            "step_count": self.step_count
        }