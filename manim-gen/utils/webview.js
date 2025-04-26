
/**
 * Returns the full HTML for the video + LaTeX display.
 * @param {vscode.Uri} videoUri - The URI of the video to display
 * @param {string} initialLatex - The LaTeX code to render on load
 * @returns {string} - The HTML string
 */

function getWebviewVideoContent(videoUri, initialLatex = 'Hello World, \\( E = mc^2 \\)') {
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Intuition Video with LaTeX</title>
      <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
      <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
      <style>
        body { margin:0; padding:20px; background:#000; color:#fff; font-family:sans-serif;
               display:flex; flex-direction:column; align-items:center; height:100vh; }
        .latex-display { font-size:18px; margin-bottom:20px; text-align:center; margin-top: 20px }
        video { width:80%; height:auto; display:block; }
      </style>
    </head>
    <body>
      <div class="latex-display" id="latexOutput">${initialLatex}</div>
      <video controls autoplay loop>
        <source src="${videoUri}" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <script>
        // Example: dynamic updates could be wired here if needed
        MathJax.typesetPromise();
      </script>
    </body>
    </html>
    `;
  }
  
  module.exports = {
    getWebviewVideoContent
  };
  