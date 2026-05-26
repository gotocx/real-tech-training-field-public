module.exports = function solve(input) {
  const intervals = (input.intervals || []).map((item) => [item[0], item[1]]);
  intervals.sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const current of intervals) {
    if (merged.length === 0 || merged[merged.length - 1][1] < current[0]) {
      merged.push(current);
    } else {
      merged[merged.length - 1][1] = Math.max(merged[merged.length - 1][1], current[1]);
    }
  }
  return merged;
};
