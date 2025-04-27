const vscode = require('vscode');
const { registerShowVideoCommand } = require('./commands/showVideo');

/**
 * Called when your extension is activated.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Extension "manim-gen" is now active!');

  // Register the "Show Video" command
  const disposable = registerShowVideoCommand(context);
  context.subscriptions.push(disposable);
}

/**
 * Called when your extension is deactivated.
 */
function deactivate() {
  console.log('Extension "manim-gen" has been deactivated.');
}

module.exports = {
  activate,
  deactivate
};
