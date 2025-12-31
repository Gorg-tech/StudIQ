/**
 * Returns the IQ level for a numeric IQ score.
 * Level = floor(score / 100)
 * @param {number} score
 * @returns {number}
 */
export function getIQLevel(score) {
  const n = Number(score) || 0;
  return Math.floor(n / getMaxPerPointsLevel());
}

/**
 * Returns remaining IQ points within the current level.
 * Points = score % 100 (normalized to 0..99)
 * @param {number} score
 * @returns {number}
 */
export function getIQPoints(score) {
  const n = Number(score) || 0;
  // normalize to positive remainder for negative inputs as well
  return ((Math.floor(n) % getMaxPerPointsLevel()) + getMaxPerPointsLevel()) % getMaxPerPointsLevel();
}

/**
 * Returns the amount of points per level
 * @returns {number}
 */
export function getMaxPerPointsLevel() {
    return 100;
}