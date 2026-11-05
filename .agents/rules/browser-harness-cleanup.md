# browser-harness-cleanup

Whenever you use `browser-harness` for a task and recordings are enabled, follow this cleanup procedure at the end of the job:
1. Keep track of the recording directory path used during the task.
2. At the end of the task, explicitly ask the user: "Do you want to keep the local browser recordings for this task, or can I delete them to save space?"
3. If the user says no (and no further debugging is needed), delete the recording directory immediately to prevent stale data from piling up.
