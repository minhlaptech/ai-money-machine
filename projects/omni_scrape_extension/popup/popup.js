/**
 * OmniScrape AI — Popup Controller & Export Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // State
  let currentTab = 'auto';
  let currentDataset = null;
  let isProUser = false;

  // DOM Elements
  const licenseBadge = document.getElementById('licenseBadge');
  const statTables = document.getElementById('statTables');
  const statEmails = document.getElementById('statEmails');
  const statPhones = document.getElementById('statPhones');
  const tabButtons = document.querySelectorAll('.tab-btn');
  const btnScrapeNow = document.getElementById('btnScrapeNow');
  const previewSection = document.getElementById('previewSection');
  const emptyState = document.getElementById('emptyState');
  const previewDatasetName = document.getElementById('previewDatasetName');
  const previewRowCount = document.getElementById('previewRowCount');
  const filterInput = document.getElementById('filterInput');
  const tableHead = document.getElementById('tableHead');
  const tableBody = document.getElementById('tableBody');
  const btnExportCsv = document.getElementById('btnExportCsv');
  const btnExportJson = document.getElementById('btnExportJson');
  const btnCopyClipboard = document.getElementById('btnCopyClipboard');
  const proPromo = document.getElementById('proPromo');
  const btnOpenUpgrade = document.getElementById('btnOpenUpgrade');
  const linkEnterKey = document.getElementById('linkEnterKey');
  const licenseModal = document.getElementById('licenseModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const licenseKeyInput = document.getElementById('licenseKeyInput');
  const btnActivateKey = document.getElementById('btnActivateKey');
  const licenseFeedback = document.getElementById('licenseFeedback');

  // 1. Initialize State & Check Pro License
  checkLicenseStatus();
  fetchPageStats();

  // Tab Switching
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTab = btn.dataset.tab;
      btnScrapeNow.querySelector('span:last-child').textContent = `Extract ${getTabLabel(currentTab)}`;
    });
  });

  // Main Extract Button
  btnScrapeNow.addEventListener('click', () => {
    executeExtraction();
  });

  // Filter Search
  filterInput.addEventListener('input', () => {
    applyFilter(filterInput.value.toLowerCase());
  });

  // Export CSV
  btnExportCsv.addEventListener('click', () => {
    if (!currentDataset || !currentDataset.rows || currentDataset.rows.length === 0) return;
    exportToCsv(currentDataset);
  });

  // Export JSON
  btnExportJson.addEventListener('click', () => {
    if (!currentDataset || !currentDataset.rows || currentDataset.rows.length === 0) return;
    exportToJson(currentDataset);
  });

  // Copy Clipboard
  btnCopyClipboard.addEventListener('click', () => {
    if (!currentDataset || !currentDataset.rows || currentDataset.rows.length === 0) return;
    copyTableToClipboard(currentDataset);
  });

  // Upgrade & License Modal
  btnOpenUpgrade.addEventListener('click', () => {
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
    activateLicense(licenseKeyInput.value.trim());
  });

  // --- Functions ---

  function getTabLabel(tab) {
    switch (tab) {
      case 'tables': return 'Tables';
      case 'lists': return 'Cards & Lists';
      case 'contacts': return 'Contacts';
      default: return 'Data From Current Page';
    }
  }

  function checkLicenseStatus() {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get(['isPro', 'licenseKey'], (res) => {
        if (res.isPro) {
          isProUser = true;
          licenseBadge.textContent = 'PRO TIER';
          licenseBadge.className = 'badge badge-pro';
          proPromo.style.display = 'none';
        }
      });
    }
  }

  function fetchPageStats() {
    sendMessageToActiveTab({ action: 'GET_PAGE_SUMMARY' }, (response) => {
      if (response && response.success && response.data) {
        const d = response.data;
        statTables.textContent = d.tableCount || 0;
        statEmails.textContent = d.emailCount || 0;
        statPhones.textContent = d.phoneCount || 0;
      }
    });
  }

  function executeExtraction() {
    btnScrapeNow.disabled = true;
    btnScrapeNow.innerHTML = '<span>⏳</span><span>Extracting Data...</span>';

    let action = 'SCRAPE_AUTO';
    if (currentTab === 'tables') action = 'SCRAPE_TABLES';
    else if (currentTab === 'lists') action = 'SCRAPE_LISTS';
    else if (currentTab === 'contacts') action = 'SCRAPE_CONTACTS';

    sendMessageToActiveTab({ action: action }, (response) => {
      btnScrapeNow.disabled = false;
      btnScrapeNow.innerHTML = '<span>🚀</span><span>Extract Data From Current Page</span>';

      if (!response || !response.success) {
        alert('Could not extract data. Make sure you are on a regular web page (not a chrome:// page).');
        return;
      }

      let dataset = null;
      if (Array.isArray(response.data) && response.data.length > 0) {
        dataset = response.data[0];
      } else if (response.data && response.data.rows) {
        dataset = response.data;
      }

      if (dataset && dataset.rows && dataset.rows.length > 0) {
        currentDataset = dataset;
        renderDataPreview(dataset);
      } else {
        alert('No structured data found for this category on this page. Try switching tabs (Tables / Cards / Contacts).');
      }
    });
  }

  function renderDataPreview(dataset) {
    emptyState.style.display = 'none';
    previewSection.style.display = 'flex';

    previewDatasetName.textContent = dataset.name || 'Extracted Dataset';
    const totalRows = dataset.rows.length;
    previewRowCount.textContent = `(${totalRows} row${totalRows > 1 ? 's' : ''})`;

    // Enforce Freemium limit (50 rows max for free tier)
    let displayRows = dataset.rows;
    if (!isProUser && totalRows > 50) {
      displayRows = dataset.rows.slice(0, 50);
      previewRowCount.textContent = `(Showing 50 of ${totalRows} rows — Free Tier)`;
    }

    // Render Table Head
    tableHead.innerHTML = '';
    const trHead = document.createElement('tr');
    (dataset.headers || []).forEach(h => {
      const th = document.createElement('th');
      th.textContent = h;
      trHead.appendChild(th);
    });
    tableHead.appendChild(trHead);

    // Render Table Body
    tableBody.innerHTML = '';
    displayRows.forEach(row => {
      const tr = document.createElement('tr');
      row.forEach(cell => {
        const td = document.createElement('td');
        td.textContent = cell;
        td.title = cell; // tooltip for truncated text
        tr.appendChild(td);
      });
      tableBody.appendChild(tr);
    });
  }

  function applyFilter(query) {
    const rows = tableBody.querySelectorAll('tr');
    rows.forEach(tr => {
      const text = tr.innerText.toLowerCase();
      tr.style.display = text.includes(query) ? '' : 'none';
    });
  }

  function exportToCsv(dataset) {
    const headers = dataset.headers || [];
    let rows = dataset.rows || [];
    if (!isProUser && rows.length > 50) {
      rows = rows.slice(0, 50);
    }

    let csvContent = '\uFEFF'; // UTF-8 BOM for Excel
    csvContent += headers.map(escapeCsvCell).join(',') + '\r\n';

    rows.forEach(r => {
      csvContent += r.map(escapeCsvCell).join(',') + '\r\n';
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const filename = `omniscrape_${sanitizeFilename(dataset.name || 'export')}_${Date.now()}.csv`;
    downloadBlob(blob, filename);
  }

  function exportToJson(dataset) {
    const headers = dataset.headers || [];
    let rows = dataset.rows || [];
    if (!isProUser && rows.length > 50) {
      rows = rows.slice(0, 50);
    }

    const jsonList = rows.map(r => {
      const obj = {};
      headers.forEach((h, i) => {
        obj[h] = r[i] || '';
      });
      return obj;
    });

    const jsonStr = JSON.stringify(jsonList, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8;' });
    const filename = `omniscrape_${sanitizeFilename(dataset.name || 'export')}_${Date.now()}.json`;
    downloadBlob(blob, filename);
  }

  function copyTableToClipboard(dataset) {
    const headers = dataset.headers || [];
    let rows = dataset.rows || [];
    if (!isProUser && rows.length > 50) {
      rows = rows.slice(0, 50);
    }

    let tsv = headers.join('\t') + '\n';
    rows.forEach(r => {
      tsv += r.join('\t') + '\n';
    });

    navigator.clipboard.writeText(tsv).then(() => {
      btnCopyClipboard.innerHTML = '<span>✓</span> Copied!';
      setTimeout(() => {
        btnCopyClipboard.innerHTML = '<span>📋</span> Copy All';
      }, 2000);
    }).catch(err => {
      alert('Could not copy to clipboard: ' + err);
    });
  }

  function escapeCsvCell(cell) {
    if (cell === null || cell === undefined) return '""';
    const str = String(cell).replace(/"/g, '""');
    return `"${str}"`;
  }

  function sanitizeFilename(name) {
    return name.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase();
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function activateLicense(key) {
    licenseFeedback.className = 'license-feedback';
    if (!key) {
      licenseFeedback.textContent = 'Please enter a license key.';
      licenseFeedback.className = 'license-feedback error';
      return;
    }

    // License key format: OMNI-PRO-XXXX-XXXX or Lemon Squeezy standard format
    const isValidFormat = (key.toUpperCase().startsWith('OMNI-PRO-') && key.length >= 15) || (key.length >= 16 && !key.includes(' '));

    if (isValidFormat) {
      if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
        chrome.storage.local.set({ isPro: true, licenseKey: key }, () => {
          licenseFeedback.textContent = '✓ Pro License Activated Successfully!';
          licenseFeedback.className = 'license-feedback success';
          setTimeout(() => {
            licenseModal.style.display = 'none';
            checkLicenseStatus();
            if (currentDataset) renderDataPreview(currentDataset);
          }, 1200);
        });
      } else {
        licenseFeedback.textContent = '✓ Pro License Activated Successfully!';
        licenseFeedback.className = 'license-feedback success';
      }
    } else {
      licenseFeedback.textContent = 'Invalid license key format. Please check your purchase email.';
      licenseFeedback.className = 'license-feedback error';
    }
  }

  function sendMessageToActiveTab(msg, callback) {
    if (typeof chrome !== 'undefined' && chrome.tabs && chrome.tabs.query) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs && tabs[0] && tabs[0].id) {
          chrome.tabs.sendMessage(tabs[0].id, msg, (response) => {
            if (chrome.runtime.lastError) {
              // Inject content script if not already injected
              chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                files: ['content/scraper.js']
              }, () => {
                chrome.tabs.sendMessage(tabs[0].id, msg, callback);
              });
            } else {
              callback(response);
            }
          });
        }
      });
    }
  }
});
