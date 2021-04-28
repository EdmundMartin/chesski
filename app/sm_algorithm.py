from datetime import datetime, timedelta
from math import ceil
from typing import Optional, Tuple


class SuperMemoAlgorithm:
    def __init__(self, ease: float, interval: int, repetitions: int) -> None:
        self.ease = ease
        self.interval = interval
        self.repetitions = repetitions if repetitions else 0
        self.review_date: Optional[datetime] = None

    @classmethod
    def first_review(cls, quality: int) -> "SuperMemoAlgorithm":
        space_rep = cls(2.5, 0, 0)
        space_rep.review(quality, datetime.now())
        return space_rep

    def _calculate_interval_reps(self, quality: int) -> Tuple[float, int]:
        if quality < 3:
            return 1, 0

        if self.repetitions == 0:
            return 1, self.repetitions + 1

        if self.repetitions == 1:
            return 6, self.repetitions + 1

        return ceil(self.interval * self.ease), self.repetitions + 1

    def review(self, quality: int, review_date: datetime) -> None:
        self.interval, self.repetitions = self._calculate_interval_reps(quality)
        self.ease += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        self.ease = max(1.3, self.ease)

        self.review_date = review_date + timedelta(self.interval)

    def __repr__(self):
        return f"<SuperMemo, Ease: {self.ease}, Reps: {self.repetitions}, Interval:{self.interval}>"