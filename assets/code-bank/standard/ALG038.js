module.exports = function solve(input) {
  const nums = input.nums;
  const k = input.k;
  if (!Array.isArray(nums) || k <= 0 || k > nums.length) return 0;
  let sum = 0;
  for (let i = 0; i < k; i += 1) sum += nums[i];
  let best = sum;
  for (let i = k; i < nums.length; i += 1) {
    sum += nums[i] - nums[i - k];
    if (sum > best) best = sum;
  }
  return best;
};
