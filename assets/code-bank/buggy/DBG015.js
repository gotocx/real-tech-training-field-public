module.exports = function solve(input) {
  const s = input.s || "";
  const last = new Map();
  let left = 0;
  let best = 0;
  for (let right = 0; right < s.length; right += 1) {
    const ch = s[right];
    if (last.has(ch) && last.get(ch) >= left) left = last.get(ch);
    last.set(ch, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
};
