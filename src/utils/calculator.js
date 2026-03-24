/**
 * Simple Calculator utility module
 * Provides basic arithmetic operations for two numbers
 */

/**
 * Adds two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 * @throws {Error} If arguments are not numbers
 */
export function add(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Both arguments must be numbers');
  }
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error('Arguments must be finite numbers');
  }
  return a + b;
}

/**
 * Subtracts second number from first
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Difference of a and b
 * @throws {Error} If arguments are not numbers
 */
export function subtract(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Both arguments must be numbers');
  }
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error('Arguments must be finite numbers');
  }
  return a - b;
}

/**
 * Multiplies two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Product of a and b
 * @throws {Error} If arguments are not numbers
 */
export function multiply(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Both arguments must be numbers');
  }
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error('Arguments must be finite numbers');
  }
  return a * b;
}

/**
 * Divides first number by second
 * @param {number} a - Numerator
 * @param {number} b - Denominator
 * @returns {number} Quotient of a and b
 * @throws {Error} If arguments are not numbers or if dividing by zero
 */
export function divide(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Both arguments must be numbers');
  }
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error('Arguments must be finite numbers');
  }
  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a / b;
}

export default {
  add,
  subtract,
  multiply,
  divide
};
