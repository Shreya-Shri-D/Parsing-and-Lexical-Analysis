from pathlib import Path

from grammar import Grammar, Rule
from utils import display, normalize, load, build_tree

_ROOT = Path(__file__).resolve().parent

class State:
    START = "<START>"

    def __init__(self, rule, dot=0, origin=0, action="", completed_by = []):
        self.rule = rule
        self.dot = dot
        self.origin = origin # position of the chart where it comes from - correlates with sentence position
        self.action = action
        self.completed_by = completed_by    # states that completed this state

    def __eq__(self, other):
        return self.rule == other.rule and self.dot == other.dot and self.origin == other.origin

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        right_side = self.rule.right_side[: self.dot] + ['*'] + self.rule.right_side[self.dot :]
        rule = f"({self.rule.left_side} -> {' '.join(right_side)}, {self.origin})"
        return "{0: <10} {1: <40}".format(self.action, rule)

    def token_by_current_dot(self):
        if self.dot < len(self.rule.right_side):
            return self.rule.right_side[self.dot]

    def is_complete(self):
        return len(self.rule.right_side) == self.dot


class Chart:
    def __init__(self):
        self.states = []  # Initialize an empty list of states for this chart

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)


class EarleyParser:
    def __init__(self, sentence, grammar):
        self.words = sentence.split()
        self.grammar = grammar

    def parse(self):
        # initialize all charts
        charts = self.create_charts(len(self.words))

        for i, chart in enumerate(charts):
            for state in chart.states:
                if self.check_predict(state):
                    self.predict(charts, i, state)
                if self.check_complete(state):
                    self.complete(charts, i, state)
                if self.check_scanner(state):
                    self.scanner(charts, i, state)
        return charts

  
    def predict(self, charts, i, state):
        token = state.token_by_current_dot()
        rules = self.grammar.get_rules(token) # [Rule(token, ...), Rule(token, ...)]
        for rule in rules:
            new_state = State(rule=rule, dot=0, origin=i, action="Predicted")
            chart = charts[i]
            chart.add_state(new_state)

 
    def scanner(self, charts, i, state):
        token = state.token_by_current_dot()
        if (i >= len(self.words)): return
        word = self.words[i]
        if (token == word):
            new_state = State(state.rule, dot=state.dot+1,origin=state.origin, action="Scanned")
            charts[i+1].add_state(new_state)

 
    def complete(self, charts, i, state):
        chart = charts[state.origin]
        left_side = state.rule.left_side
        for origin_state in chart.states:
            if (self.check_left_side_in_right_side(origin_state, left_side)):
                new_state = State(origin_state.rule, dot=origin_state.dot+1,
                            origin=origin_state.origin,
                            action="Completed",
                            completed_by=origin_state.completed_by + [state]
                            )
                current_chart = charts[i]
                current_chart.add_state(new_state)

    # true, if dot stays behind the token in the origin state, where token == left_side
    def check_left_side_in_right_side(self, origin_state, left_side): # True/False
        return origin_state.token_by_current_dot() == left_side

    def check_predict(self, state): # True/False
        # state is not complete
        # right token from dot - is non terminal
        return not state.is_complete() and not self.grammar.is_terminal(state.token_by_current_dot())

    def check_scanner(self, state): # True/False
        # state is not complete
        # right token from dot - is terminal
        return not state.is_complete() and self.grammar.is_terminal(state.token_by_current_dot())
    
    def check_complete(self, state): # True/False
        # state is complete
        return state.is_complete()

    def create_charts(self, num):
        # creation of fake chart
        fake_rule = Rule(left_side=State.START, right_side=[self.grammar.start])
        fake_state = State(fake_rule, dot=0, origin=0, action="Started")
        fake_chart = Chart()
        fake_chart.add_state(fake_state)

        charts = []
        charts.append(fake_chart)

        # creation of real charts
        for i in range(num):
            charts.append(Chart())

        return charts

def main():
    ## PROCESS INPUT
    grammar = Grammar.load_grammar(str(_ROOT / "grammatik.txt"))
    sentence = normalize(load(str(_ROOT / "input.txt")))  # remove punctuation , . ' ' etc

    ## PARSE INPUT
    parser = EarleyParser(sentence, grammar)
    charts = parser.parse() 

    ## PRINT RESULT
    # parser.chart - list
    # i - index of chart in list, char - element of parser.chart
    for i, chart in enumerate(charts):
        print("-" * 50, f"Chart #{i}", "-"*50)
        for state in chart.states:
            # print (10 spaces + state.action) (40 spaces + state) (slice sentence from i-position till end)
            print("{0: <50} {1} ".format(str(state), " ".join(sentence.split()[i:])))

    ## build tree and visualize    
    tree = build_tree(State.START, charts, grammar)
    display(tree, sentence, render=True)


# startpoint in python
if __name__ == "__main__":
    main()
