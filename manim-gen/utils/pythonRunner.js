const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

/**
 * Runs a Python script and returns its stdout output.
 * Will prompt for GEMINI_API_KEY if not stored in SecretStorage.
 * @param {vscode.ExtensionContext} context - Extension context for SecretStorage
 * @param {string} scriptName - Relative path (from extension root) to the script
 * @param {string[]} args - Command-line arguments to pass to the script
 * @returns {Promise<string>} - Resolves with stdout, rejects on error or non-zero exit
 */
async function runPythonScript(context, scriptName, args = []) {
  // 1) Compute script path
  const scriptPath = path.join(__dirname, '..', scriptName);

  // 2) Retrieve or prompt for API key
  let apiKey = await context.secrets.get('geminiApiKey');
  if (!apiKey) {
    apiKey = await vscode.window.showInputBox({
      prompt: 'Enter your GEMINI_API_KEY',
      ignoreFocusOut: true,
      password: true
    });
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY is required to run this command.');
    }
    // Store for future runs
    await context.secrets.store('geminiApiKey', apiKey);
  }

  // 3) Build env with the API key
  const childEnv = { ...process.env, GEMINI_API_KEY: apiKey };

  // 4) Spawn Python and capture output
  return new Promise((resolve, reject) => {
    const py = spawn('python', [scriptPath, ...args], {
      cwd: path.dirname(scriptPath),
      env: childEnv,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    py.stdout.on('data', data => { stdout += data.toString(); });
    py.stderr.on('data', data => { stderr += data.toString(); });

    py.on('close', code => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        reject(new Error(`Python exited ${code}: ${stderr}`));
      }
    });
  });
}

module.exports = { runPythonScript };