module.exports = function solve(input) {
  const nums = input.nums || [];
  const k = input.k || 0;
  const count = new Map();
  for (const num of nums) count.set(num, (count.get(num) || 0) + 1);
  return [...count.entries()]
    .sort((a, b) => b[1] - a[1] || a[0] - b[0])
    .slice(0, k)
    .map((item) => item[0]);
};
