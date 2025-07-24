// API Base URL
const API_BASE = '/api';

// Global variables
let currentDocuments = [];
let queryHistory = JSON.parse(localStorage.getItem('queryHistory') || '[]');

// Utility Functions
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner"></div><p>Loading...</p>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<p style="color: #e74c3c;">❌ ${message}</p>`;
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Stats Functions
async function loadStats() {
    try {
        const stats = await apiRequest('/documents/stats');
        
        document.getElementById('totalDocs').textContent = stats.total_documents;
        document.getElementById('totalSize').textContent = stats.total_size_mb + ' MB';
    } catch (error) {
        console.error('Failed to load stats:', error);
        document.getElementById('totalDocs').textContent = 'Error';
        document.getElementById('totalSize').textContent = 'Error';
    }
}

function refreshStats() {
    loadStats();
    loadRecentDocuments();
}

// Document Functions
async function loadRecentDocuments() {
    try {
        const response = await apiRequest('/documents?per_page=5');
        currentDocuments = response.documents;
        displayRecentDocuments(response.documents);
    } catch (error) {
        console.error('Failed to load recent documents:', error);
        showError('recentDocs', 'Failed to load recent documents');
    }
}

function displayRecentDocuments(documents) {
    const container = document.getElementById('recentDocs') || document.getElementById('recentUploads');
    
    if (!container) return;
    
    if (documents.length === 0) {
        container.innerHTML = '<p>No documents uploaded yet.</p>';
        return;
    }
    
    container.innerHTML = documents.map(doc => `
        <div class="document-card">
            <div class="document-title">📄 ${doc.original_filename}</div>
            <div class="document-meta">
                Uploaded: ${formatDate(doc.upload_date)} | Size: ${formatFileSize(doc.file_size)}
            </div>
            ${doc.description ? `<div class="document-description">${doc.description}</div>` : ''}
            ${doc.tags && doc.tags.length > 0 ? `<div class="document-tags">Tags: ${doc.tags.join(', ')}</div>` : ''}
            <div class="document-actions">
                <button class="btn btn-primary" onclick="queryDocument(${doc.id})">Query</button>
                <button class="btn btn-secondary" onclick="deleteDocument(${doc.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function loadDocuments() {
    try {
        const response = await apiRequest('/documents');
        currentDocuments = response.documents;
        displayDocuments(response.documents);
        populateDocumentSelect(response.documents);
    } catch (error) {
        console.error('Failed to load documents:', error);
        showError('documentList', 'Failed to load documents');
    }
}

function displayDocuments(documents) {
    const container = document.getElementById('documentList');
    
    if (!container) return;
    
    if (documents.length === 0) {
        container.innerHTML = '<p>No documents available. <a href="/upload">Upload some PDFs</a> to get started!</p>';
        return;
    }
    
    container.innerHTML = documents.map(doc => `
        <div class="document-card">
            <div class="document-title">📄 ${doc.original_filename}</div>
            <div class="document-meta">
                ID: ${doc.id} | Uploaded: ${formatDate(doc.upload_date)} | Size: ${formatFileSize(doc.file_size)}
            </div>
            ${doc.description ? `<div class="document-description">${doc.description}</div>` : ''}
            ${doc.tags && doc.tags.length > 0 ? `<div class="document-tags">Tags: ${doc.tags.join(', ')}</div>` : ''}
        </div>
    `).join('');
}

function populateDocumentSelect(documents) {
    const select = document.getElementById('documentSelect');
    
    if (!select) return;
    
    // Clear existing options except the first one
    select.innerHTML = '<option value="">Query All Documents</option>';
    
    documents.forEach(doc => {
        const option = document.createElement('option');
        option.value = doc.id;
        option.textContent = doc.original_filename;
        select.appendChild(option);
    });
}

async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }
    
    try {
        await apiRequest(`/documents/${documentId}`, { method: 'DELETE' });
        alert('Document deleted successfully!');
        loadRecentDocuments();
        loadDocuments();
        loadStats();
    } catch (error) {
        console.error('Failed to delete document:', error);
        alert('Failed to delete document: ' + error.message);
    }
}

// Upload Functions
function setupUploadForm() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    
    if (!form || !fileInput) return;
    
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = '';
        }
    });
    
    form.addEventListener('submit', handleUpload);
}

async function handleUpload(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const progressDiv = document.getElementById('uploadProgress');
    const resultDiv = document.getElementById('uploadResult');
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Show progress
    progressDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    
    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Show success
        resultDiv.innerHTML = `
            <div class="upload-result success">
                ✅ Upload successful!
                <br><strong>File:</strong> ${result.document.original_filename}
                <br><strong>Size:</strong> ${formatFileSize(result.document.file_size)}
                <br><strong>ID:</strong> ${result.document.id}
            </div>
        `;
        resultDiv.style.display = 'block';
        
        // Reset form
        form.reset();
        document.getElementById('fileName').textContent = '';
        
        // Refresh data
        loadRecentDocuments();
        loadStats();
        
    } catch (error) {
        console.error('Upload failed:', error);
        resultDiv.innerHTML = `
            <div class="upload-result error">
                ❌ Upload failed: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        progressDiv.style.display = 'none';
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload PDF';
    }
}

// Query Functions
function setupQueryForm() {
    const form = document.getElementById('queryForm');
    
    if (!form) return;
    
    form.addEventListener('submit', handleQuery);
}

async function handleQuery(event) {
    event.preventDefault();
    
    const queryInput = document.getElementById('queryInput');
    const documentSelect = document.getElementById('documentSelect');
    const queryBtn = document.getElementById('queryBtn');
    const loadingDiv = document.getElementById('queryLoading');
    const resultDiv = document.getElementById('queryResult');
    
    const query = queryInput.value.trim();
    const documentId = documentSelect ? documentSelect.value : '';
    
    if (!query) {
        alert('Please enter a question.');
        return;
    }
    
    if (query.length < 3) {
        alert('Query must be at least 3 characters long.');
        return;
    }
    
    // Show enhanced loading message
    loadingDiv.style.display = 'block';
    loadingDiv.innerHTML = '<div class="loading-spinner"></div><p>🤖 AI is analyzing your documents...</p>';
    resultDiv.style.display = 'none';
    queryBtn.disabled = true;
    queryBtn.textContent = 'Processing...';
    
    try {
        const requestBody = { query };
        if (documentId) {
            requestBody.document_id = parseInt(documentId);
        }
        
        const response = await apiRequest('/query', {
            method: 'POST',
            body: JSON.stringify(requestBody)
        });
        
        // Enhanced result display
        if (response.success !== false && response.answer) {
            displayEnhancedQueryResult(response, query, documentId);
        } else {
            document.getElementById('responseText').innerHTML = `
                <div class="error-message">
                    <h3>❌ Error</h3>
                    <p>${response.error || 'Failed to process query'}</p>
                </div>
            `;
            document.getElementById('resultMeta').textContent = '';
        }
        
        resultDiv.style.display = 'block';
        
        // Add to history
        addToQueryHistory(query, response.answer || response.error, documentId);
        
    } catch (error) {
        console.error('Query failed:', error);
        document.getElementById('responseText').innerHTML = `
            <div class="error-message">
                <h3>❌ Network Error</h3>
                <p>Failed to connect to the server. Please try again.</p>
            </div>
        `;
        document.getElementById('resultMeta').textContent = '';
        resultDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
        queryBtn.disabled = false;
        queryBtn.textContent = 'Ask AI';
    }
}

function displayEnhancedQueryResult(response, query, documentId) {
    const responseText = document.getElementById('responseText');
    const resultMeta = document.getElementById('resultMeta');
    
    // Format the AI response
    let formattedAnswer = formatAIResponse(response.answer);
    
    // Create enhanced response HTML
    let html = `
        <div class="ai-response">
            <div class="query-header">
                <h3>🤖 AI Response</h3>
                <p class="query-text"><strong>Your Question:</strong> "${query}"</p>
            </div>
            
            <div class="ai-answer">
                <div class="answer-content">${formattedAnswer}</div>
            </div>
        </div>
    `;
    
    // Add AI actions
    html += `
        <div class="ai-actions">
            <button onclick="generateAllSummaries()" class="btn btn-outline">📝 Generate Summaries</button>
            <button onclick="extractAllKeywords()" class="btn btn-outline">🏷️ Extract Keywords</button>
            <button onclick="clearQueryResults()" class="btn btn-secondary">Clear</button>
        </div>
    `;
    
    responseText.innerHTML = html;
    
    // Enhanced metadata
    let metaText = `Query: "${query}"`;
    
    if (documentId) {
        metaText += ` | Document: ID ${documentId}`;
    } else {
        metaText += ' | Searched: All documents';
    }
    
    if (response.documents_searched) {
        metaText += ` | Found: ${response.documents_searched} documents`;
    }
    
    if (response.model_used) {
        metaText += ` | AI Model: ${response.model_used}`;
    }
    
    if (response.tokens_used) {
        metaText += ` | Tokens: ${response.tokens_used}`;
    }
    
    resultMeta.textContent = metaText;
}

function formatAIResponse(response) {
    if (!response) return 'No response available';
    
    // Convert newlines to HTML breaks and format the response
    return response
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p>')
        .replace(/$/, '</p>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
        .replace(/\*(.*?)\*/g, '<em>$1</em>');  // Italic text
}

async function generateAllSummaries() {
    const responseText = document.getElementById('responseText');
    const originalContent = responseText.innerHTML;
    
    try {
        responseText.innerHTML = '<div class="loading-spinner"></div><p>🤖 Generating summaries...</p>';
        
        const documents = await apiRequest('/documents');
        
        if (!documents.documents || documents.documents.length === 0) {
            responseText.innerHTML = '<p>No documents available for summary generation.</p>';
            return;
        }
        
        let summariesHtml = '<div class="summaries-container"><h3>📝 Document Summaries</h3>';
        
        for (const doc of documents.documents) {
            try {
                const summaryResponse = await apiRequest(`/documents/${doc.id}/summary`, {
                    method: 'POST'
                });
                
                summariesHtml += `
                    <div class="summary-item">
                        <h4>📄 ${doc.original_filename}</h4>
                        <div class="summary-content">${summaryResponse.summary || 'Summary not available'}</div>
                    </div>
                `;
            } catch (error) {
                summariesHtml += `
                    <div class="summary-item error">
                        <h4>📄 ${doc.original_filename}</h4>
                        <div class="error-content">Failed to generate summary</div>
                    </div>
                `;
            }
        }
        
        summariesHtml += `
            <div class="action-buttons">
                <button onclick="restoreQueryResults(\`${originalContent.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)" class="btn btn-secondary">Back to Results</button>
            </div>
        </div>`;
        
        responseText.innerHTML = summariesHtml;
        
    } catch (error) {
        responseText.innerHTML = originalContent;
        alert('Failed to generate summaries. Please try again.');
        console.error('Summary generation error:', error);
    }
}

async function extractAllKeywords() {
    const responseText = document.getElementById('responseText');
    const originalContent = responseText.innerHTML;
    
    try {
        responseText.innerHTML = '<div class="loading-spinner"></div><p>🤖 Extracting keywords...</p>';
        
        const documents = await apiRequest('/documents');
        
        if (!documents.documents || documents.documents.length === 0) {
            responseText.innerHTML = '<p>No documents available for keyword extraction.</p>';
            return;
        }
        
        let keywordsHtml = '<div class="keywords-container"><h3>🏷️ Document Keywords</h3>';
        
        for (const doc of documents.documents) {
            try {
                const keywordsResponse = await apiRequest(`/documents/${doc.id}/keywords`, {
                    method: 'POST'
                });
                
                const keywords = keywordsResponse.keywords || [];
                const keywordTags = keywords.map(kw => `<span class="keyword-tag">${kw}</span>`).join(' ');
                
                keywordsHtml += `
                    <div class="keywords-item">
                        <h4>📄 ${doc.original_filename}</h4>
                        <div class="keywords-content">${keywordTags || 'No keywords available'}</div>
                    </div>
                `;
            } catch (error) {
                keywordsHtml += `
                    <div class="keywords-item error">
                        <h4>📄 ${doc.original_filename}</h4>
                        <div class="error-content">Failed to extract keywords</div>
                    </div>
                `;
            }
        }
        
        keywordsHtml += `
            <div class="action-buttons">
                <button onclick="restoreQueryResults(\`${originalContent.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)" class="btn btn-secondary">Back to Results</button>
            </div>
        </div>`;
        
        responseText.innerHTML = keywordsHtml;
        
    } catch (error) {
        responseText.innerHTML = originalContent;
        alert('Failed to extract keywords. Please try again.');
        console.error('Keywords extraction error:', error);
    }
}

function restoreQueryResults(content) {
    const responseText = document.getElementById('responseText');
    responseText.innerHTML = content;
}

function clearQueryResults() {
    const queryInput = document.getElementById('queryInput');
    const responseText = document.getElementById('responseText');
    const resultDiv = document.getElementById('queryResult');
    
    if (queryInput) queryInput.value = '';
    if (responseText) responseText.innerHTML = '';
    if (resultDiv) resultDiv.style.display = 'none';
}

function queryDocument(documentId) {
    // Navigate to query page with pre-selected document
    window.location.href = `/query?doc=${documentId}`;
}

// Query History Functions
function addToQueryHistory(query, response, documentId) {
    const historyItem = {
        query,
        response,
        documentId,
        timestamp: new Date().toISOString()
    };
    
    queryHistory.unshift(historyItem);
    
    // Keep only last 10 queries
    if (queryHistory.length > 10) {
        queryHistory = queryHistory.slice(0, 10);
    }
    
    localStorage.setItem('queryHistory', JSON.stringify(queryHistory));
    displayQueryHistory();
}

function displayQueryHistory() {
    const container = document.getElementById('queryHistory');
    const clearBtn = document.getElementById('clearHistoryBtn');
    
    if (!container) return;
    
    if (queryHistory.length === 0) {
        container.innerHTML = '<p>No queries yet. Ask your first question!</p>';
        if (clearBtn) clearBtn.style.display = 'none';
        return;
    }
    
    // Show clear button when there are queries
    if (clearBtn) clearBtn.style.display = 'inline-block';
    
    container.innerHTML = queryHistory.map(item => `
        <div class="query-history-item">
            <div class="query-text">Q: ${item.query}</div>
            <div class="query-response">A: ${item.response}</div>
            <div class="query-time">
                ${formatDate(item.timestamp)} 
                ${item.documentId ? `| Document ID: ${item.documentId}` : '| All documents'}
            </div>
        </div>
    `).join('');
}

function clearQueryHistory() {
    if (confirm('Are you sure you want to clear all query history? This action cannot be undone.')) {
        queryHistory = [];
        localStorage.removeItem('queryHistory');
        displayQueryHistory();
    }
}

function loadQueryHistory() {
    displayQueryHistory();
}

// Initialize page based on URL parameters
function initializePage() {
    const urlParams = new URLSearchParams(window.location.search);
    const docId = urlParams.get('doc');
    
    if (docId && document.getElementById('documentSelect')) {
        // Pre-select document if specified in URL
        setTimeout(() => {
            document.getElementById('documentSelect').value = docId;
        }, 1000);
    }
}

// Page load initialization
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

// Export functions for global use
window.refreshStats = refreshStats;
window.deleteDocument = deleteDocument;
window.clearQueryHistory = clearQueryHistory;
window.queryDocument = queryDocument;
window.setQuery = function(text) {
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.value = text;
    }
};
