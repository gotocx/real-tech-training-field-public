module.exports = function solve(input) {
  const grid = input.grid || [];
  if (grid.length === 0 || grid[0].length === 0) return 0;
  const dp = Array(grid[0].length).fill(Infinity);
  dp[0] = 0;
  for (let r = 0; r < grid.length; r += 1) {
    for (let c = 0; c < grid[r].length; c += 1) {
      if (c === 0) dp[c] = dp[c] + grid[r][c];
      else dp[c] = Math.max(dp[c], dp[c - 1]) + grid[r][c];
    }
  }
  return dp[dp.length - 1];
};
