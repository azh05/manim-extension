
const vscode = require('vscode');
const { registerShowVideoCommand } = require('./commands/showVideo');

/**
 * Called when the extension is activated.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  // Log activation for diagnostic purposes
  console.log('Extension "manim-gen" is now active!');

  // Register the "Show Test Video" command and add its disposable to subscriptions
  const showVideoDisposable = registerShowVideoCommand(context);
  context.subscriptions.push(showVideoDisposable);
}

/**
 * Called when the extension is deactivated.
 */
function deactivate() {
  console.log('Extension "manim-gen" has been deactivated.');
}

module.exports = {
  activate,
  deactivate
};
