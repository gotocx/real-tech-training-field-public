module.exports = function solve(input) {
  const nums = input.nums || [];
  const result = Array(nums.length).fill(1);
  let prefix = 1;
  for (let i = 0; i < nums.length; i += 1) {
    result[i] = prefix;
    prefix *= nums[i];
  }
  let suffix = 1;
  for (let i = nums.length - 1; i >= 0; i -= 1) {
    result[i] += suffix;
    suffix *= nums[i];
  }
  return result;
};
