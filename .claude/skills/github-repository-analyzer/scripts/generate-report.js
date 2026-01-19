/**
 * GitHub Repository Analyzer - Report Generation Helper
 * 
 * This script demonstrates how to generate markdown and HTML reports
 * following the NetworkPage design system.
 */

const fs = require('fs');
const path = require('path');

/**
 * Generate timestamp for filenames
 * @returns {string} Timestamp in format YYYYMMDD-HHmmss
 */
function getTimestamp() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}${month}${day}-${hours}${minutes}${seconds}`;
}

/**
 * Sanitize repository name for use in filename
 * @param {string} repoName - Repository name
 * @returns {string} Sanitized name
 */
function sanitizeRepoName(repoName) {
    return repoName
        .toLowerCase()
        .replace(/[^a-z0-9-]/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
}

/**
 * Generate markdown report filename
 * @param {string} repoName - Repository name
 * @returns {string} Filename
 */
function getMarkdownFilename(repoName) {
    const sanitized = sanitizeRepoName(repoName);
    const timestamp = getTimestamp();
    return `${sanitized}-analysis-${timestamp}.md`;
}

/**
 * Generate HTML report filename
 * @param {string} repoName - Repository name
 * @returns {string} Filename
 */
function getHtmlFilename(repoName) {
    const sanitized = sanitizeRepoName(repoName);
    const timestamp = getTimestamp();
    return `${sanitized}-analysis-${timestamp}.html`;
}

/**
 * Save markdown report to file
 * @param {string} content - Markdown content
 * @param {string} repoName - Repository name
 * @param {string} outputDir - Output directory
 * @returns {Promise<string>} File path of saved file
 */
async function saveMarkdownReport(content, repoName, outputDir = '.') {
    const filename = getMarkdownFilename(repoName);
    const filepath = path.resolve(outputDir, filename);
    
    await fs.promises.writeFile(filepath, content, 'utf8');
    return filepath;
}

/**
 * Generate HTML report from markdown content
 * @param {string} markdown - Markdown content
 * @param {string} repoName - Repository name
 * @param {string} outputDir - Output directory
 * @returns {Promise<string>} File path of saved HTML file
 */
async function generateHtmlReport(markdown, repoName, outputDir = '.') {
    const templatePath = path.resolve(__dirname, 'report-template.html');
    const filename = getHtmlFilename(repoName);
    const filepath = path.resolve(outputDir, filename);
    
    // Read template
    const template = await fs.promises.readFile(templatePath, 'utf8');
    
    // Replace markdown placeholder
    const html = template.replace('{{MARKDOWN_CONTENT}}', markdown);
    
    // Write HTML file
    await fs.promises.writeFile(filepath, html, 'utf8');
    
    return filepath;
}

/**
 * Complete report generation process
 * @param {string} markdownContent - The markdown report content
 * @param {string} repoName - Repository name
 * @param {string} outputDir - Output directory (default: current directory)
 * @returns {Promise<{markdown: string, html: string}>} Paths to generated files
 */
async function generateCompleteReport(markdownContent, repoName, outputDir = '.') {
    // Ensure output directory exists
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Generate markdown report
    const markdownPath = await saveMarkdownReport(markdownContent, repoName, outputDir);
    console.log(`✓ Markdown report saved to: ${markdownPath}`);
    
    // Generate HTML report
    const htmlPath = await generateHtmlReport(markdownContent, repoName, outputDir);
    console.log(`✓ HTML report saved to: ${htmlPath}`);
    
    return {
        markdown: markdownPath,
        html: htmlPath
    };
}

/**
 * Example usage
 */
async function example() {
    const sampleMarkdown = `# Executive Summary
This is a comprehensive analysis of the example repository.

## Repository Overview
- Repository Name: example/repo
- Description: An example repository for testing
- Stars: 1000

## Technology Stack Analysis
### Primary Technologies
- JavaScript
- Node.js
- React

## Code Quality Assessment
### Structure
The repository follows best practices for organization.

### Quality Metrics
- Code Coverage: 85%
- Linting: ESLint

## Architecture Analysis
### System Architecture
The project uses a modular architecture.

## Community and Ecosystem
### Activity Metrics
- Contributors: 50
- Active Issues: 12

## Trends and Future Development
### Development Velocity
Active development with frequent releases.

## Strengths
- Well-documented
- Active community
- Good test coverage

## Weaknesses and Risks
- Some outdated dependencies
- Limited documentation for advanced features

## Recommendations
1. Update dependencies to latest versions
2. Improve advanced feature documentation
3. Add more integration tests
`;

    try {
        const result = await generateCompleteReport(sampleMarkdown, 'example/repo', './output');
        console.log('\n📊 Report generation complete!');
        console.log(`📄 Markdown: ${result.markdown}`);
        console.log(`🌐 HTML: ${result.html}`);
    } catch (error) {
        console.error('❌ Error generating reports:', error);
    }
}

// Export functions for use in skill
module.exports = {
    getTimestamp,
    sanitizeRepoName,
    getMarkdownFilename,
    getHtmlFilename,
    saveMarkdownReport,
    generateHtmlReport,
    generateCompleteReport
};

// Run example if executed directly
if (require.main === module) {
    example();
}
