from __future__ import annotations
import re

class StatelessBaseline:
    name='stateless'
    def __init__(self): self.work_time=None; self.goal=False
    def observe(self,msg):
        if re.search(r'\b(?:my goal is|i want to|i need to)\b',msg,re.I): self.goal=True
    def current_work_time(self): return None

class FirstMentionMemoryBaseline:
    name='first_mention_memory'
    def __init__(self): self.work_time=None; self.goal=False
    def observe(self,msg):
        l=msg.lower()
        if self.work_time is None and ('prefer' in l or 'works better' in l):
            if 'morning' in l: self.work_time='morning'
            elif 'evening' in l: self.work_time='evening'
        if re.search(r'\b(?:my goal is|i want to|i need to)\b',msg,re.I): self.goal=True
    def current_work_time(self): return self.work_time
