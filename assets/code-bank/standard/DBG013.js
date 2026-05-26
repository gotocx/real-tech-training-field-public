module.exports = function solve(input) {
  const nums = input.nums;
  const target = input.target;
  const seen = new Map();
  for (let i = 0; i < nums.length; i += 1) {
    const need = target - nums[i];
    if (seen.has(need)) return [seen.get(need), i];
    if (!seen.has(nums[i])) seen.set(nums[i], i);
  }
  return [];
};
