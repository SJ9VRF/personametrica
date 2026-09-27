from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import defaultdict
import random, statistics
from typing import Iterable

from personalagi.user_model.probabilistic_belief import PersonalBeliefState, PreferenceEvidence

DOMAINS = {
    "work_time": ("morning", "evening"),
    "response_detail": ("concise", "detailed"),
    "travel_pace": ("structured", "spontaneous"),
    "restaurant_noise": ("quiet", "lively"),
    "notification_style": ("batch", "immediate"),
    "budget_style": ("save", "premium"),
    "exercise_time": ("morning", "evening"),
    "meeting_style": ("agenda", "open_discussion"),
    "reading_depth": ("summary", "deep_dive"),
    "planning_style": ("early", "last_minute"),
}
LANGUAGES = ["en", "es", "fr", "fa", "zh"]

@dataclass(slots=True)
class Observation:
    user_id: str
    turn: int
    slot: str
    value: str
    source: str
    confidence: float
    context: str | None = None
    temporary_until: int | None = None
    changes_truth: bool = False
    language: str = "en"
    provenance: str = ""

    def evidence(self) -> PreferenceEvidence:
        return PreferenceEvidence(
            slot=self.slot, value=self.value, turn=self.turn, source=self.source,
            confidence=self.confidence, context=self.context,
            temporary_until=self.temporary_until, provenance=self.provenance,
        )

@dataclass(slots=True)
class Query:
    user_id: str
    turn: int
    slot: str
    expected: str
    context: str | None = None
    split: str = "standard"

@dataclass(slots=True)
class BenchmarkConfig:
    users: int = 500
    turns: int = 240
    seed: int = 31
    noise_rate: float = 0.10
    implicit_rate: float = 0.22
    temporary_rate: float = 0.24
    query_every: int = 24
    behavior_noise_rate: float = 0.22
    languages: tuple[str, ...] = tuple(LANGUAGES)

class FirstMentionTracker:
    name = "first-mention"
    def __init__(self): self.state = {}
    def observe(self, o: Observation):
        self.state.setdefault(o.slot, o.value)
    def read(self, q: Query): return self.state.get(q.slot), 1.0 if q.slot in self.state else 0.0

class LatestObservationTracker:
    name = "latest-observation"
    def __init__(self): self.state = {}
    def observe(self, o: Observation): self.state[o.slot] = o.value
    def read(self, q: Query): return self.state.get(q.slot), 1.0 if q.slot in self.state else 0.0

class SlidingWindowTracker:
    name = "sliding-window-40"
    def __init__(self, window=40): self.window=window; self.rows=[]
    def observe(self, o: Observation): self.rows.append(o)
    def read(self, q: Query):
        rows=[o for o in self.rows if o.slot==q.slot and q.turn-o.turn <= self.window]
        return (rows[-1].value, 1.0) if rows else (None,0.0)

class TrustedLatestTracker:
    """Strong non-probabilistic structured-memory baseline.

    It ignores obvious hypothetical/other-person distractors but lacks explicit expiry
    semantics, uncertainty aggregation, and evidence competition.
    """
    name = "trusted-latest"
    def __init__(self): self.state={}
    def observe(self, o: Observation):
        if o.source not in {"hypothetical","other_person"}:
            self.state[o.slot]=(o.value,o.confidence)
    def read(self,q: Query): return self.state.get(q.slot,(None,0.0))

class TimeAwareLatestTracker:
    """Strong structured baseline with explicit temporary-scope semantics.

    Unlike trusted-latest, this baseline keeps general and temporary evidence separate
    and checks expiry at read time. It does not aggregate competing evidence or learn
    confidence; it is intended as a strong symbolic baseline rather than a strawman.
    """
    name = "time-aware-latest"
    def __init__(self): self.rows=[]
    def observe(self,o: Observation):
        if o.source not in {"hypothetical","other_person"}: self.rows.append(o)
    def read(self,q: Query):
        rows=[o for o in self.rows if o.slot==q.slot and o.turn<=q.turn]
        if q.context is not None:
            scoped=[o for o in rows if o.context==q.context and (o.temporary_until is None or q.turn<=o.temporary_until)]
            if scoped:
                o=scoped[-1]; return o.value,o.confidence
        general=[o for o in rows if o.context is None]
        if not general: return None,0.0
        o=general[-1]; return o.value,o.confidence

class BeliefStateTracker:
    name = "personal-belief-state"
    def __init__(self): self.pbs=PersonalBeliefState(half_life_turns=90,temperature=.20)
    def observe(self,o: Observation): self.pbs.update(o.evidence())
    def read(self,q: Query):
        r=self.pbs.read(q.slot,turn=q.turn,context=q.context)
        return r.value,r.confidence

TRACKERS=(FirstMentionTracker,LatestObservationTracker,SlidingWindowTracker,TrustedLatestTracker,TimeAwareLatestTracker,BeliefStateTracker)


def _alternative(slot: str, current: str) -> str:
    a,b=DOMAINS[slot]
    return b if current==a else a


def generate_user_stream(user_idx: int, cfg: BenchmarkConfig) -> tuple[list[Observation],list[Query]]:
    r=random.Random(cfg.seed*100003 + user_idx)
    uid=f"pbs-s{cfg.seed:05d}-u{user_idx:05d}"
    slots=list(DOMAINS)
    truth={s:r.choice(DOMAINS[s]) for s in slots}
    base_truth=dict(truth)
    observations=[]; queries=[]
    # initial evidence spread across first 20 turns
    schedule=defaultdict(list)
    for i,s in enumerate(slots):
        t=1+i*2
        schedule[t].append(("initial",s))
    # every user gets 4-7 durable preference changes
    for s in r.sample(slots,r.randint(4,7)):
        t=r.randint(55,max(60,cfg.turns-55))
        schedule[t].append(("reversal",s))
    # temporary exceptions: useful because latest-memory baselines keep them after expiry
    for s in r.sample(slots,max(1,int(len(slots)*cfg.temporary_rate))):
        start=r.randint(70,max(75,cfg.turns-45)); end=min(cfg.turns,start+r.randint(12,28))
        schedule[start].append(("temporary",s,end))
    for turn in range(1,cfg.turns+1):
        for item in schedule.get(turn,[]):
            kind,s,*rest=item
            lang=r.choice(cfg.languages)
            if kind=="initial":
                observations.append(Observation(uid,turn,s,truth[s],"explicit",.98,language=lang,provenance="initial-explicit"))
            elif kind=="reversal":
                truth[s]=_alternative(s,truth[s])
                src="implicit_choice" if r.random()<cfg.implicit_rate else "explicit"
                conf=.78 if src=="implicit_choice" else .97
                observations.append(Observation(uid,turn,s,truth[s],src,conf,changes_truth=True,language=lang,provenance="durable-change"))
            elif kind=="temporary":
                end=rest[0]; temp=_alternative(s,truth[s])
                observations.append(Observation(uid,turn,s,temp,"explicit",.96,context="temporary",temporary_until=end,language=lang,provenance="temporary-exception"))
        # Noisy observations do not alter hidden truth.
        if r.random()<cfg.noise_rate:
            s=r.choice(slots); bogus=_alternative(s,truth[s]); src=r.choice(["hypothetical","other_person"])
            observations.append(Observation(uid,turn,s,bogus,src,.92,language=r.choice(cfg.languages),provenance="distractor"))
        # weaker implicit behavioral evidence usually supports current truth
        if r.random()<cfg.implicit_rate/4:
            s=r.choice(slots)
            observed = _alternative(s, truth[s]) if r.random() < cfg.behavior_noise_rate else truth[s]
            observations.append(Observation(uid,turn,s,observed,"implicit_behavior",.64,language=r.choice(cfg.languages),provenance="behavioral-cue"))
        if turn>=30 and turn%cfg.query_every==0:
            for s in r.sample(slots,3):
                expected=truth[s]
                context=None
                # During an active temporary exception, a scoped query should prefer it.
                active_temp=[o for o in observations if o.slot==s and o.context=="temporary" and o.turn<=turn and o.temporary_until and turn<=o.temporary_until]
                if active_temp and r.random()<.5:
                    expected=active_temp[-1].value; context="temporary"
                queries.append(Query(uid,turn,s,expected,context=context))
    return observations,queries


def _evaluate_tracker(tracker_cls, streams: list[tuple[list[Observation],list[Query]]], *, action_threshold: float = .70, defer_cost: float = .10):
    total=correct=acted=acted_correct=asks=0
    confidences=[]; correctness=[]
    by_source=defaultdict(lambda:[0,0])
    for observations,queries in streams:
        tracker=tracker_cls()
        events=sorted([(o.turn,0,o) for o in observations]+[(q.turn,1,q) for q in queries], key=lambda x:(x[0],x[1]))
        for _,kind,obj in events:
            if kind==0: tracker.observe(obj)
            else:
                pred,conf=tracker.read(obj); ok=pred==obj.expected
                total+=1; correct+=int(ok); confidences.append(float(conf)); correctness.append(int(ok))
                # Uncertainty-aware downstream action: ask/defer below 0.70.
                if conf<action_threshold or pred is None: asks+=1
                else: acted+=1; acted_correct+=int(ok)
                bucket="temporary" if obj.context else "general"
                by_source[bucket][0]+=int(ok); by_source[bucket][1]+=1
    acc=correct/max(1,total)
    coverage=acted/max(1,total)
    selective=acted_correct/max(1,acted)
    # Utility: correct action +1, incorrect action -1, asking costs 0.10.
    utility=(acted_correct - (acted-acted_correct) - defer_cost*asks)/max(1,total)
    brier=sum((c-y)**2 for c,y in zip(confidences,correctness))/max(1,total)
    return {
        "accuracy":acc,"coverage":coverage,"selective_accuracy":selective,
        "decision_utility":utility,"ask_rate":asks/max(1,total),"brier":brier,
        "queries":total,
        "slices":{k:v[0]/max(1,v[1]) for k,v in by_source.items()},
    }


def run_benchmark(cfg: BenchmarkConfig, *, action_threshold: float = .70, defer_cost: float = .10) -> dict:
    streams=[generate_user_stream(i,cfg) for i in range(cfg.users)]
    results={cls.name:_evaluate_tracker(cls,streams, action_threshold=action_threshold, defer_cost=defer_cost) for cls in TRACKERS}
    return {"config":asdict(cfg),"evaluation":{"action_threshold":action_threshold,"defer_cost":defer_cost},"results":results}


def run_distribution_shifts(seed=31) -> dict:
    configs={
        "standard":BenchmarkConfig(users=500,turns=240,seed=seed),
        "high_noise":BenchmarkConfig(users=250,turns=240,seed=seed+1,noise_rate=.28),
        "implicit_heavy":BenchmarkConfig(users=250,turns=240,seed=seed+2,implicit_rate=.55),
        "temporary_heavy":BenchmarkConfig(users=250,turns=240,seed=seed+3,temporary_rate=.60),
        "long_horizon":BenchmarkConfig(users=180,turns=800,seed=seed+4,query_every=50),
    }
    return {name:run_benchmark(cfg) for name,cfg in configs.items()}
