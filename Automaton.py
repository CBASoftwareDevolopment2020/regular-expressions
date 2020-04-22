from queue import LifoQueue
from Bag import Bag


class Digraph():
    def __init__(self, V: int):
        self._V = V
        self._E = 0
        self._adj = Bag()
        for v in range(V):
            self._adj.add(Bag())

    @property
    def V(self):
        return self._V

    @property
    def E(self):
        return self._E

    def addEdge(self, v: int, w: int):
        self._adj[v].add(w)
        self._E += 1

    def adj(self, v) -> iter:
        return self._adj[v]

    def reverse(self):
        R = Digraph(self._V)
        for v in range(self._V):
            for w in self._adj:
                R.addEdge(w, v)
        return R


class DirectedDFS:
    def __init__(self, G: Digraph, sources: iter):
        self._marked = [False] * G.V
        for s in sources:
            if not self._marked[s]:
                self.dfs(G, s)

    def dfs(self, G: Digraph, v: int):
        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self.dfs(G, w)

    def marked(self, v) -> bool:
        return self._marked[v]


class NFA:
    def __init__(self, regexp: str):
        ops = LifoQueue()
        self._re = list(regexp)
        self._M = len(self._re)
        self._G = Digraph(self._M + 1)

        for i in range(self._M):
            lp = i
            if self._re[i] == '(' or self._re[i] == '|':
                ops.put(i)
            elif self._re[i] == ')':
                _or = ops.get()
                if self._re[i] == '|':
                    lp = ops.get()
                    self._G.addEdge(lp, i + 1)
                    self._G.addEdge(_or, i)
                else:
                    lp = _or

            if i < self._M - 1 and self._re[i + 1] == '*':
                self._G.addEdge(lp, i + 1)
                self._G.addEdge(i + 1, lp)
            if self._re[i] in "(*)":
                self._G.addEdge(i, i + 1)

    def recognizes(self, txt: str) -> bool:
        dfs = DirectedDFS(self._G, [0])
        pc = Bag([v for v in range(self._G.V) if dfs.marked(v)])

        for i in range(len(txt)):
            match = Bag([v + 1 for v in pc if v < self._M and self._re[v] in '.' + txt[i]])
            dfs = DirectedDFS(self._G, match)
            pc = Bag([v for v in range(self._G.V) if dfs.marked(v)])

        return self._M in pc


if __name__ == '__main__':
    regex = '.*'
    nfa = NFA(regex)
    txts = ['hej', 'med', 'dig']
    for txt in txts:
        if nfa.recognizes(txt):
            print(txt)
