module.exports = function solve(input) {
  const s = input.s || "";
  const t = input.t || "";
  if (s.length !== t.length) return false;
  const count = new Map();
  for (const ch of s) count.set(ch, (count.get(ch) || 0) + 1);
  for (const ch of t) {
    const next = (count.get(ch) || 0) - 1;
    if (next < 0) return true;
    count.set(ch, next);
  }
  return true;
};
