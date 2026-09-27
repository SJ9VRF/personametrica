from personalagi.user_model.probabilistic_belief import PersonalBeliefState, PreferenceEvidence
from personalbench.belief_benchmark import BenchmarkConfig, run_benchmark

def test_hypothetical_does_not_override_explicit():
    p=PersonalBeliefState()
    p.update(PreferenceEvidence('food','vegetarian',1,'explicit',.98))
    p.update(PreferenceEvidence('food','omnivore',2,'hypothetical',.99))
    r=p.read('food',turn=3)
    assert r.value=='vegetarian'
    assert r.confidence>.75

def test_temporary_exception_expires():
    p=PersonalBeliefState()
    p.update(PreferenceEvidence('work','morning',1,'explicit',.98))
    p.update(PreferenceEvidence('work','evening',10,'explicit',.98,context='temporary',temporary_until=20))
    assert p.read('work',turn=15,context='temporary').value=='evening'
    assert p.read('work',turn=40,context=None).value=='morning'

def test_benchmark_pbs_beats_first_mention():
    out=run_benchmark(BenchmarkConfig(users=40,turns=120,seed=2,query_every=20))['results']
    assert out['personal-belief-state']['accuracy'] > out['first-mention']['accuracy']
    assert out['personal-belief-state']['decision_utility'] > out['first-mention']['decision_utility']
