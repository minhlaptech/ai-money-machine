/**
 * SnapOCR Pro — Core Processing Engine & Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // State
  let currentImageBlob = null;
  let ocrWorker = null;
  let isProUser = false;
  let extractedRawText = '';
  let extractedTableRows = [];

  // DOM Elements
  const dropZone = document.getElementById('dropZone');
  const dropPrompt = document.getElementById('dropPrompt');
  const previewWrap = document.getElementById('previewWrap');
  const imagePreview = document.getElementById('imagePreview');
  const fileInput = document.getElementById('fileInput');
  const btnPasteClipboard = document.getElementById('btnPasteClipboard');
  const btnRemoveImage = document.getElementById('btnRemoveImage');
  const btnRunOcr = document.getElementById('btnRunOcr');
  const langSelect = document.getElementById('langSelect');
  const modeSelect = document.getElementById('modeSelect');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const outputTextArea = document.getElementById('outputTextArea');
  const charCount = document.getElementById('charCount');
  const wordCount = document.getElementById('wordCount');
  const confidenceScore = document.getElementById('confidenceScore');
  const tablePreviewContainer = document.getElementById('tablePreviewContainer');
  const translatedTextArea = document.getElementById('translatedTextArea');
  const btnTranslateNow = document.getElementById('btnTranslateNow');
  const targetLang = document.getElementById('targetLang');
  const statusMessage = document.getElementById('statusMessage');
  const tierBadge = document.getElementById('tierBadge');
  const btnUpgradeNav = document.getElementById('btnUpgradeNav');
  const linkEnterKey = document.getElementById('linkEnterKey');
  const licenseModal = document.getElementById('licenseModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const licenseInput = document.getElementById('licenseInput');
  const btnActivateKey = document.getElementById('btnActivateKey');
  const licenseFeedback = document.getElementById('licenseFeedback');
  const navTabs = document.querySelectorAll('.nav-tab');
  const btnCopyText = document.getElementById('btnCopyText');
  const btnExportCsv = document.getElementById('btnExportCsv');
  const btnExportMarkdown = document.getElementById('btnExportMarkdown');
  const btnClearAll = document.getElementById('btnClearAll');

  // Check Pro Status
  checkProStatus();

  // Tab Navigation
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      navTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const targetPane = tab.dataset.tab;
      document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
      if (targetPane === 'text') document.getElementById('paneText').style.display = 'flex';
      if (targetPane === 'table') document.getElementById('paneTable').style.display = 'flex';
      if (targetPane === 'translate') document.getElementById('paneTranslate').style.display = 'flex';
    });
  });

  // Global Paste Listener (Ctrl+V)
  window.addEventListener('paste', (e) => {
    handlePasteEvent(e);
  });

  btnPasteClipboard.addEventListener('click', async () => {
    try {
      const clipboardItems = await navigator.clipboard.read();
      for (const item of clipboardItems) {
        for (const type of item.types) {
          if (type.startsWith('image/')) {
            const blob = await item.getType(type);
            loadImageBlob(blob);
            setStatus('Pasted image from clipboard!');
            return;
          }
        }
      }
      alert('No image found in clipboard. Press Win+Shift+S to snip an image first, then paste!');
    } catch (err) {
      alert('Clipboard permission denied or browser does not support clipboard.read(). Please press Ctrl+V directly.');
    }
  });

  // File Input
  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      loadImageBlob(e.target.files[0]);
    }
  });

  // Drag & Drop
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadImageBlob(e.dataTransfer.files[0]);
    }
  });

  btnRemoveImage.addEventListener('click', () => {
    clearInputImage();
  });

  // Run OCR
  btnRunOcr.addEventListener('click', () => {
    executeOcr();
  });

  // Copy Buttons
  btnCopyText.addEventListener('click', () => {
    if (!outputTextArea.value) return;
    navigator.clipboard.writeText(outputTextArea.value);
    setStatus('Copied text to clipboard!');
  });

  btnExportCsv.addEventListener('click', () => {
    exportCsv();
  });

  btnExportMarkdown.addEventListener('click', () => {
    exportMarkdown();
  });

  btnClearAll.addEventListener('click', () => {
    clearAllData();
  });

  // Translate
  btnTranslateNow.addEventListener('click', () => {
    translateCurrentText();
  });

  // Modals & Upgrade
  btnUpgradeNav.addEventListener('click', () => {
    window.open('https://minhlap.lemonsqueezy.com', '_blank');
  });

  linkEnterKey.addEventListener('click', (e) => {
    e.preventDefault();
    licenseModal.style.display = 'flex';
  });

  btnCloseModal.addEventListener('click', () => {
    licenseModal.style.display = 'none';
  });

  btnActivateKey.addEventListener('click', () => {
    activateLicense(licenseInput.value.trim());
  });

  // Output text change listener for counters
  outputTextArea.addEventListener('input', () => {
    updateCounters(outputTextArea.value);
  });

  // --- Core Functions ---

  function handlePasteEvent(e) {
    if (e.clipboardData && e.clipboardData.items) {
      const items = e.clipboardData.items;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          loadImageBlob(blob);
          setStatus('Clipboard image loaded! Click "Run OCR Extraction" to process.');
          break;
        }
      }
    }
  }

  function loadImageBlob(blob) {
    currentImageBlob = blob;
    const url = URL.createObjectURL(blob);
    imagePreview.src = url;
    dropPrompt.style.display = 'none';
    previewWrap.style.display = 'flex';
    btnRunOcr.disabled = false;
    setStatus('Image ready. Select language and click Run OCR Extraction.');
  }

  function clearInputImage() {
    currentImageBlob = null;
    imagePreview.src = '';
    dropPrompt.style.display = 'block';
    previewWrap.style.display = 'none';
    btnRunOcr.disabled = true;
    fileInput.value = '';
    setStatus('Engine ready. Waiting for input image or clipboard paste.');
  }

  async function executeOcr() {
    if (!currentImageBlob) return;

    btnRunOcr.disabled = true;
    progressWrap.style.display = 'flex';
    progressBar.style.width = '10%';
    progressText.textContent = 'Loading AI OCR engine...';
    setStatus('Processing OCR...');

    const selectedLang = langSelect.value;
    const selectedMode = modeSelect.value;

    try {
      if (typeof Tesseract === 'undefined') {
        throw new Error('Tesseract OCR library not loaded. Check internet connection or CSP.');
      }

      const result = await Tesseract.recognize(
        currentImageBlob,
        selectedLang,
        {
          logger: m => {
            if (m.status === 'recognizing text') {
              const p = Math.round(m.progress * 100);
              progressBar.style.width = `${p}%`;
              progressText.textContent = `Recognizing text: ${p}%`;
            } else {
              progressText.textContent = m.status;
            }
          }
        }
      );

      progressBar.style.width = '100%';
      progressText.textContent = 'Extraction complete!';
      setTimeout(() => { progressWrap.style.display = 'none'; }, 800);

      extractedRawText = result.data.text;
      const confidence = Math.round(result.data.confidence);

      let processedText = cleanOcrText(extractedRawText, selectedMode);
      outputTextArea.value = processedText;
      updateCounters(processedText, confidence);

      // Generate Table Data if in table or auto mode
      if (selectedMode === 'table' || (processedText.includes('\t') || processedText.includes('|'))) {
        parseTableData(processedText);
      }

      setStatus(`OCR succeeded (${confidence}% confidence)! Extracted ${processedText.length} characters.`);
    } catch (err) {
      progressWrap.style.display = 'none';
      alert(`OCR Error: ${err.message}`);
      setStatus(`OCR failed: ${err.message}`);
    } finally {
      btnRunOcr.disabled = false;
    }
  }

  function cleanOcrText(raw, mode) {
    if (!raw) return '';
    let text = raw.replace(/\r\n/g, '\n');

    if (mode === 'single_line') {
      return text.replace(/\n+/g, ' ').trim();
    }
    if (mode === 'code') {
      return text;
    }
    // Auto clean paragraphs: remove erratic breaks while preserving empty lines
    return text.split('\n\n').map(p => p.replace(/\n/g, ' ').trim()).join('\n\n').trim();
  }

  function parseTableData(text) {
    const lines = text.split('\n').filter(l => l.trim().length > 0);
    if (lines.length === 0) return;

    // Detect delimiter: pipe, tab, or multi-space
    const rows = lines.map(line => {
      if (line.includes('|')) {
        return line.split('|').map(c => c.trim()).filter((c, i, a) => !(i === 0 && c === '') && !(i === a.length - 1 && c === ''));
      } else if (line.includes('\t')) {
        return line.split('\t').map(c => c.trim());
      } else {
        return line.split(/\s{2,}/).map(c => c.trim());
      }
    });

    extractedTableRows = rows;
    renderTablePreview(rows);
  }

  function renderTablePreview(rows) {
    if (!rows || rows.length === 0) {
      tablePreviewContainer.innerHTML = '<p class="empty-table-msg">No tabular structure detected.</p>';
      return;
    }

    const headers = rows[0];
    const dataRows = rows.slice(1);

    let html = '<table class="fluent-table"><thead><tr>';
    headers.forEach((h, i) => {
      html += `<th>${h || 'Col ' + (i + 1)}</th>`;
    });
    html += '</tr></thead><tbody>';

    dataRows.forEach(r => {
      html += '<tr>';
      headers.forEach((_, i) => {
        html += `<td>${r[i] || ''}</td>`;
      });
      html += '</tr>';
    });
    html += '</tbody></table>';

    tablePreviewContainer.innerHTML = html;
  }

  function updateCounters(text, confidence = null) {
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
    if (confidence !== null) {
      confidenceScore.textContent = `Confidence: ${confidence}%`;
    }
  }

  function exportCsv() {
    let rows = extractedTableRows;
    if (rows.length === 0) {
      // Fallback: convert lines to single-column CSV
      rows = outputTextArea.value.split('\n').map(l => [l]);
    }
    if (rows.length === 0) return;

    let csv = '\uFEFF'; // BOM
    rows.forEach(r => {
      csv += r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',') + '\r\n';
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `snapocr_export_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    setStatus('Exported CSV successfully!');
  }

  function exportMarkdown() {
    if (extractedTableRows.length > 0) {
      let md = '';
      const headers = extractedTableRows[0];
      md += '| ' + headers.join(' | ') + ' |\n';
      md += '| ' + headers.map(() => '---').join(' | ') + ' |\n';
      extractedTableRows.slice(1).forEach(r => {
        md += '| ' + headers.map((_, i) => r[i] || '').join(' | ') + ' |\n';
      });
      navigator.clipboard.writeText(md);
      setStatus('Copied Markdown table to clipboard!');
    } else {
      navigator.clipboard.writeText(outputTextArea.value);
      setStatus('Copied Markdown text to clipboard!');
    }
  }

  async function translateCurrentText() {
    const text = outputTextArea.value.trim();
    if (!text) {
      alert('Please run OCR extraction first to get text to translate.');
      return;
    }

    const tLang = targetLang.value;
    translatedTextArea.value = 'Translating...';
    setStatus(`Translating to ${tLang.toUpperCase()}...`);

    try {
      // Free public translation API bridge
      const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text.slice(0, 500))}&langpair=autodetect|${tLang}`;
      const res = await fetch(url);
      const json = await res.json();
      if (json && json.responseData && json.responseData.translatedText) {
        translatedTextArea.value = json.responseData.translatedText;
        setStatus('Translation completed!');
      } else {
        throw new Error('Could not translate text.');
      }
    } catch (e) {
      translatedTextArea.value = `[Offline Fallback Mode]: Could not reach translation server (${e.message}). You can copy the extracted text and paste into Google Translate.`;
      setStatus('Translation failed or offline.');
    }
  }

  function clearAllData() {
    clearInputImage();
    outputTextArea.value = '';
    translatedTextArea.value = '';
    extractedRawText = '';
    extractedTableRows = [];
    tablePreviewContainer.innerHTML = '<p class="empty-table-msg">Run OCR with "Table" structure to view tabular rows and columns here.</p>';
    updateCounters('');
    setStatus('All data cleared.');
  }

  function checkProStatus() {
    const savedKey = localStorage.getItem('snapocr_pro_license');
    if (savedKey) {
      isProUser = true;
      tierBadge.textContent = 'PRO TIER (UNLIMITED)';
      tierBadge.className = 'tier-badge tier-pro';
      btnUpgradeNav.style.display = 'none';
    }
  }

  function activateLicense(key) {
    licenseFeedback.className = 'feedback-msg';
    if (!key) {
      licenseFeedback.textContent = 'Please enter a valid license key.';
      licenseFeedback.className = 'feedback-msg error';
      return;
    }

    const isValid = (key.toUpperCase().startsWith('SNAP-PRO-') && key.length >= 15) || (key.length >= 16 && !key.includes(' '));

    if (isValid) {
      localStorage.setItem('snapocr_pro_license', key);
      licenseFeedback.textContent = '✓ Pro Lifetime License Activated Successfully!';
      licenseFeedback.className = 'feedback-msg success';
      setTimeout(() => {
        licenseModal.style.display = 'none';
        checkProStatus();
        setStatus('Welcome to SnapOCR Pro! Unlimited scans enabled.');
      }, 1200);
    } else {
      licenseFeedback.textContent = 'Invalid license key format. Please check your purchase confirmation.';
      licenseFeedback.className = 'feedback-msg error';
    }
  }

  function setStatus(msg) {
    statusMessage.textContent = msg;
  }
});
