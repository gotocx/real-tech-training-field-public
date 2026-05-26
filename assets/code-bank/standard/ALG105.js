module.exports = function solve(input) {
  const coins = input.coins || [];
  const amount = input.amount || 0;
  const dp = Array(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (let value = 1; value <= amount; value += 1) {
    for (const coin of coins) {
      if (value >= coin) dp[value] = Math.min(dp[value], dp[value - coin] + 1);
    }
  }
  return Number.isFinite(dp[amount]) ? dp[amount] : -1;
};
