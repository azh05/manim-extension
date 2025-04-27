/**
 * @param {vscode.WebviewPanel} panel
 * @param {vscode.Uri} videoUri
 * @param {string} initialLatex
 */
function getWebviewVideoContent(panel, videoUri, initialLatex = 'Hello \\(E=mc^2\\)') {
  const csp = `
    default-src 'none';
    media-src ${panel.webview.cspSource} blob:;
    script-src ${panel.webview.cspSource} https://cdn.jsdelivr.net;
    style-src  ${panel.webview.cspSource} 'unsafe-inline';
    img-src    ${panel.webview.cspSource} https:;
  `.replace(/\s+/g, ' ').trim();

  return `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="${csp}">
    <title>Intuition Video</title>

    <!-- MathJax -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async 
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>

    <style>
      body { margin:0; padding:20px; background:#000; color:#fff;
             font-family:sans-serif; display:flex;
             flex-direction:column; align-items:center; height:100vh; }
      .latex-display { font-size:18px; margin:20px 0; text-align:center; }
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
      MathJax.typesetPromise();
    </script>
  </body>
  </html>
  `;
}

module.exports = { getWebviewVideoContent };
