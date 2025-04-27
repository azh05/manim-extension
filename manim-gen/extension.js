const vscode = require('vscode');
const path = require('path');
const { registerShowVideoCommand } = require('./commands/showVideo');

/**
 * Called when your extension is activated.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Extension "manim-gen" is now active!');

  // 1. Register the existing "Show Video" command
  const disposable = registerShowVideoCommand(context);
  context.subscriptions.push(disposable);

}

function deactivate() {}

function getWebviewVideoContent(videoUri, initialLatex = '\\( E = mc^2 \\)') {
	return `
	  <!DOCTYPE html>
	  <html lang="en">
	  <head>
		<meta charset="UTF-8">
		<title>Test Video with LaTeX</title>
		<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
		<script id="MathJax-script" async
		  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
		</script>
		<style>
		  body {
			margin: 0; padding: 20px; background: #000;
			color: #fff; font-family: sans-serif;
			display: flex; flex-direction: column;
			align-items: center; height: 100vh;
		  }
		  .latex-display { font-size: 24px; margin-bottom: 20px; }
		  input { width: 80%; padding: 8px; font-size: 16px; }
		  video { width: 80%; border: 2px solid #fff; }
		</style>
	  </head>
	  <body>
		<input id="latexInput" type="text"
		  value="${initialLatex}"
		  placeholder="Enter LaTeX (e.g. \\( x^2 \\))">
		<div class="latex-display" id="latexOutput">
		  ${initialLatex}
		</div>
		<video controls autoplay loop>
		  <source src="${videoUri}" type="video/mp4">
		</video>
		<script>
		  const input = document.getElementById('latexInput');
		  const output = document.getElementById('latexOutput');
		  input.addEventListener('input', () => {
			output.textContent = input.value || '${initialLatex}';
			MathJax.typesetPromise();
		  });
		</script>
	  </body>
	  </html>
	`;
  }
  
  module.exports = { activate, deactivate };

module.exports = {
  activate,
  deactivate
};
