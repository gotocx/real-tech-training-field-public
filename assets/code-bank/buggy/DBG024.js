module.exports = function solve(input) {
  const n = input.n || 0;
  const edges = input.prerequisites || [];
  const graph = Array.from({ length: n }, () => []);
  const indegree = Array(n).fill(0);
  for (const [course, pre] of edges) {
    graph[pre].push(course);
    indegree[course] += 1;
  }
  const queue = [];
  for (let i = 0; i < n; i += 1) if (indegree[i] === 0) queue.push(i);
  let visited = 0;
  while (queue.length > 0) {
    const node = queue.shift();
    visited += 1;
    for (const next of graph[node]) {
      indegree[next] -= 1;
      if (indegree[next] === 0) queue.push(next);
    }
  }
  return visited !== n;
};
