
const vscode = require('vscode');
const { convertDollarToMathJax } = require('../utils/latex');
const { getWebviewVideoContent } = require('../utils/webview');

/**
 * Registers the "Show Video" command and returns its Disposable.
 * @param {vscode.ExtensionContext} context
 * @returns {vscode.Disposable}
 */
function registerShowVideoCommand(context) {
  return vscode.commands.registerCommand(
    'manim-gen.showVideo',
    async () => {
      // Get the active text editor and any selected LaTeX code
      const editor = vscode.window.activeTextEditor;
      const selectedText = editor ? editor.document.getText(editor.selection) : '';

      // Default to a sample formula if nothing is selected
      const rawLatex = selectedText || 'E = mc^2';

      // Convert dólar-style delimiters to MathJax format
      const safeLatex = convertDollarToMathJax(rawLatex);
      console.log('Converted LaTeX:', safeLatex);

      // Create and show a WebviewPanel to display the video and rendered LaTeX
      const panel = vscode.window.createWebviewPanel(
        'video',                   // internal identifier
        'Intuition Video with LaTeX',       // user-facing title
        vscode.ViewColumn.One,         // display in first column
        {
          enableScripts: true,
          localResourceRoots: [
            vscode.Uri.joinPath(context.extensionUri, 'media')
          ]
        }
      );

      // Construct URI to the bundled video file
      const videoPath = vscode.Uri.joinPath(
        context.extensionUri,
        'media',
        'test.mp4'
      );
      const videoSrc = panel.webview.asWebviewUri(videoPath);

      // Set the HTML content of the panel
      panel.webview.html = getWebviewVideoContent(videoSrc, safeLatex);
    }
  );
}

module.exports = {
  registerShowVideoCommand
};

