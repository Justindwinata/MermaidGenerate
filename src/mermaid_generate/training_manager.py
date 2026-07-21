"""Threaded training job manager for the Gradio UI."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from .training import FineTuningConfig, TrainingResult, run_fine_tuning


@dataclass
class TrainingJobState:
    job_id: str
    status: str = "idle"
    progress: float = 0.0
    logs: list[str] = field(default_factory=list)
    latest_metrics: dict[str, Any] = field(default_factory=dict)
    result: TrainingResult | None = None
    cancel_requested: bool = False
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.result is not None:
            payload["result"] = asdict(self.result)
        return payload


class TrainingManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._jobs: dict[str, TrainingJobState] = {}
        self._active_job_id: str | None = None

    def start(
        self,
        samples: list[dict[str, Any]],
        config: FineTuningConfig,
    ) -> str:
        with self._lock:
            if self._active_job_id is not None:
                raise RuntimeError("Another fine-tuning job is already running.")
            job_id = uuid.uuid4().hex
            state = TrainingJobState(job_id=job_id, status="validating_dataset")
            self._jobs[job_id] = state
            self._active_job_id = job_id

        thread = threading.Thread(
            target=self._run_job,
            args=(job_id, samples, config),
            daemon=True,
        )
        thread.start()
        return job_id

    def _append_log(self, job_id: str, message: str) -> None:
        with self._lock:
            state = self._jobs[job_id]
            state.logs.append(message)
            state.updated_at = time.time()

    def _progress_callback(self, job_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            state = self._jobs[job_id]
            if "status" in payload:
                state.status = str(payload["status"])
            if "progress" in payload:
                state.progress = max(0.0, min(1.0, float(payload["progress"])))
            state.latest_metrics = payload
            state.updated_at = time.time()
            if "loss" in payload or "eval_loss" in payload:
                state.logs.append(str(payload))
            if "warning" in payload:
                state.logs.append(str(payload["warning"]))

    def _should_cancel(self, job_id: str) -> bool:
        with self._lock:
            return self._jobs[job_id].cancel_requested

    def _run_job(
        self,
        job_id: str,
        samples: list[dict[str, Any]],
        config: FineTuningConfig,
    ) -> None:
        try:
            if not samples:
                raise ValueError("Training requires at least one valid sample.")
            result = run_fine_tuning(
                samples,
                config,
                report_progress=lambda payload: self._progress_callback(job_id, payload),
                should_cancel=lambda: self._should_cancel(job_id),
            )
            with self._lock:
                state = self._jobs[job_id]
                state.result = result
                state.status = result.status
                state.progress = 1.0 if result.status == "completed" else state.progress
                state.error = result.message if result.status == "failed" else None
                state.updated_at = time.time()
        except Exception as exc:
            with self._lock:
                state = self._jobs[job_id]
                state.status = "failed"
                state.error = str(exc)
                state.logs.append(str(exc))
                state.updated_at = time.time()
        finally:
            with self._lock:
                if self._active_job_id == job_id:
                    self._active_job_id = None

    def cancel(self, job_id: str) -> None:
        with self._lock:
            state = self._jobs.get(job_id)
            if state is None:
                raise KeyError(f"Training job not found: {job_id}")
            if state.status not in {
                "validating_dataset",
                "loading_model",
                "preparing_dataset",
                "training",
            }:
                raise RuntimeError("Training job is not cancellable in its current state.")
            state.status = "cancelling"
            state.cancel_requested = True
            state.updated_at = time.time()

    def get(self, job_id: str) -> TrainingJobState | None:
        with self._lock:
            return self._jobs.get(job_id)

    def clear(self) -> None:
        with self._lock:
            if self._active_job_id is not None:
                raise RuntimeError("Cannot clear state while training is running.")
            self._jobs.clear()


TRAINING_MANAGER = TrainingManager()
