
/**
 * Convert dollar-style LaTeX delimiters into MathJax delimiters:
 *   $$…$$ → \[…\]   (display math)
 *    $…$  → \(...\) (inline math)
 * Preserves literal "\$" by using a temporary placeholder.
 *
 * @param {string} input - The raw text containing LaTeX code
 * @returns {string} - The sanitized string with MathJax delimiters
 */

function convertDollarToMathJax(input) {
    const ESC = '__ESCAPED_DOLLAR__';
    let s = input.replace(/\\\$/g, ESC);
  
    // Replace display math
    s = s.replace(/\$\$([\s\S]+?)\$\$/g, (_match, content) => `\\[${content.trim()}\\]`);
  
    // Replace inline math
    s = s.replace(/\$([^$\n][^$]*?)\$/g, (_match, content) => `\\(${content.trim()}\\)`);
  
    // Restore escaped dollars
    return s.replace(new RegExp(ESC, 'g'), '\\\$');
  }
  
  module.exports = {
    convertDollarToMathJax
  };