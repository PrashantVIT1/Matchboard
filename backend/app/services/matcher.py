from app.core.config import get_n_suitable_candidates


class MatcherService:
    def __init__(self, n, job_description):
        self.job_description = job_description
        self.n_suitable_candidates = n

    def set_job_description(self, job_description):
        self.job_description = job_description
    def get_n_suitable_candidates(self):
        return get_n_suitable_candidates(self.n_suitable_candidates,self.job_description)

