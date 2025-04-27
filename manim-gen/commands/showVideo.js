
const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const { convertDollarToMathJax } = require('../utils/latex');
const { getWebviewVideoContent } = require('../utils/webview');
const { runPythonScript } = require('../utils/pythonRunner');

/**
 * Registers the "Show Video" command and returns its Disposable.
 * @param {vscode.ExtensionContext} context
 * @returns {vscode.Disposable}
 */
function registerShowVideoCommand(context) {
  return vscode.commands.registerCommand(
    'manim-gen.showVideo',
    async () => {
      // 1) Retrieve selected LaTeX or fallback
      const editor = vscode.window.activeTextEditor;
      const rawLatex = editor
        ? editor.document.getText(editor.selection) || 'E = mc^2'
        : 'E = mc^2';

      // 2) Sanitize delimiters for MathJax
      const safeLatex = convertDollarToMathJax(rawLatex);

      // 3) Ensure output directory under global storage
      const outDirUri = vscode.Uri.joinPath(context.globalStorageUri, 'manim-output');
      const outDir = outDirUri.fsPath;
      try {
        await fs.promises.mkdir(outDir, { recursive: true });
      } catch (err) {
        vscode.window.showErrorMessage(`Failed to create output directory: ${err.message}`);
        return;
      }

      vscode.window.showInformationMessage("Generating Latex Video and Tab")

      // 4) Run the Python script, which should print the path to the generated video
      const videoFilePath = vscode.Uri.joinPath(
        context.globalStorageUri, "manim-output.mp4"
      )
      
      try {
        const result = await runPythonScript(
          context,
          'manim-scripts/make_animation.py',
          [safeLatex, outDir]
        );

        console.log(result)
      } catch (err) {
        console.log(err.message)
        vscode.window.showErrorMessage(`Error running Python: ${err.message}`);
        return;
      }

        // 5) Create and show a Webview panel with the video and LaTeX
        const panel = vscode.window.createWebviewPanel(
            'videoLatex',
            'Visualization with Manim',
            vscode.ViewColumn.One,
            {
                enableScripts: true,                       // for MathJax
                localResourceRoots: [
                    context.globalStorageUri,                // allow loading from /…/globalStorage/ext-id/
                ]
            }
        );

      // Convert local video file path into a Webview URI
      let videoUri;
      try {
        videoUri = panel.webview.asWebviewUri(videoFilePath);
      } catch {
        vscode.window.showErrorMessage(`Invalid video path returned: ${videoFilePath}`);
        return;
      }

      // 6) Set HTML content
      panel.webview.html = panel.webview.html = getWebviewVideoContent(panel, videoUri, safeLatex);
    }
  );
}

module.exports = { registerShowVideoCommand };