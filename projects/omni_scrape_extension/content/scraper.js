/**
 * OmniScrape AI — Content Script Scraper Engine
 * Runs in the context of the active web page to extract structured tabular data.
 */

(function () {
  // Listen for messages from extension popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    try {
      if (request.action === 'GET_PAGE_SUMMARY') {
        const summary = getPageSummary();
        sendResponse({ success: true, data: summary });
      } else if (request.action === 'SCRAPE_TABLES') {
        const tablesData = extractHtmlTables();
        sendResponse({ success: true, data: tablesData });
      } else if (request.action === 'SCRAPE_LISTS') {
        const listsData = extractRepeatingLists();
        sendResponse({ success: true, data: listsData });
      } else if (request.action === 'SCRAPE_CONTACTS') {
        const contactsData = extractContacts();
        sendResponse({ success: true, data: contactsData });
      } else if (request.action === 'SCRAPE_AUTO') {
        // Auto mode: check tables first, if none or weak, check repeating lists
        const tables = extractHtmlTables();
        if (tables.length > 0 && tables[0].rows.length > 1) {
          sendResponse({ success: true, type: 'tables', data: tables });
        } else {
          const lists = extractRepeatingLists();
          if (lists.length > 0 && lists[0].rows.length > 0) {
            sendResponse({ success: true, type: 'lists', data: lists });
          } else {
            const contacts = extractContacts();
            sendResponse({ success: true, type: 'contacts', data: contacts });
          }
        }
      }
    } catch (err) {
      sendResponse({ success: false, error: err.message });
    }
    return true; // Keep message channel open for async response
  });

  function getPageSummary() {
    const tableElements = document.querySelectorAll('table');
    let totalTableRows = 0;
    tableElements.forEach(t => {
      totalTableRows += t.querySelectorAll('tr').length;
    });

    const contacts = extractContacts();

    return {
      title: document.title || 'Untitled Page',
      url: window.location.href,
      tableCount: tableElements.length,
      tableRowsEstimate: totalTableRows,
      emailCount: contacts.emails.length,
      phoneCount: contacts.phones.length
    };
  }

  function extractHtmlTables() {
    const tables = document.querySelectorAll('table');
    const results = [];

    tables.forEach((table, tableIdx) => {
      // Skip hidden tables
      if (table.offsetParent === null && table.offsetWidth === 0 && table.offsetHeight === 0) {
        return;
      }

      const rows = Array.from(table.querySelectorAll('tr'));
      if (rows.length === 0) return;

      let headers = [];
      const dataRows = [];

      // Check for th headers in the first row or thead
      const ths = table.querySelectorAll('thead th, tr:first-child th');
      if (ths.length > 0) {
        headers = Array.from(ths).map((th, i) => th.innerText.trim() || `Column_${i + 1}`);
      }

      rows.forEach((tr, rowIdx) => {
        const cells = Array.from(tr.querySelectorAll('th, td'));
        if (cells.length === 0) return;

        const rowValues = cells.map(c => cleanText(c.innerText));

        // If no headers were found yet, use first row as headers
        if (headers.length === 0 && rowIdx === 0) {
          headers = rowValues.map((v, i) => v || `Column_${i + 1}`);
        } else if (rowIdx > 0 || ths.length > 0) {
          // Add data row if it has content
          if (rowValues.some(v => v.length > 0)) {
            dataRows.push(rowValues);
          }
        }
      });

      // Normalize row lengths to match headers length
      const maxCols = Math.max(headers.length, ...dataRows.map(r => r.length));
      while (headers.length < maxCols) {
        headers.push(`Column_${headers.length + 1}`);
      }

      if (dataRows.length > 0) {
        results.push({
          name: table.getAttribute('id') || table.getAttribute('aria-label') || `Table #${tableIdx + 1}`,
          headers: headers,
          rows: dataRows
        });
      }
    });

    return results;
  }

  function extractRepeatingLists() {
    // Look for parent containers with multiple repeating child elements (e.g., cards, products, search results)
    const candidates = document.querySelectorAll('ul, ol, div, section, main');
    const detected = [];

    candidates.forEach(parent => {
      const children = Array.from(parent.children).filter(c => {
        return c.offsetWidth > 50 && c.offsetHeight > 20 && c.tagName !== 'SCRIPT' && c.tagName !== 'STYLE';
      });

      // Need at least 3 similar repeating items
      if (children.length >= 3) {
        const tag = children[0].tagName;
        const className = children[0].className;
        const isHomogeneous = children.slice(1).every(c => c.tagName === tag && (!className || c.className === className));

        if (isHomogeneous && children.length <= 500) {
          const items = [];
          children.forEach(card => {
            const item = {};

            // Title / Heading
            const heading = card.querySelector('h1, h2, h3, h4, h5, h6, [class*="title"], [class*="name"]');
            if (heading) item['Title'] = cleanText(heading.innerText);

            // Link
            const link = card.tagName === 'A' ? card : card.querySelector('a[href]');
            if (link && link.href) item['Link'] = link.href;

            // Price
            const price = card.querySelector('[class*="price"], [class*="amount"], [class*="cost"]');
            if (price) {
              item['Price'] = cleanText(price.innerText);
            } else {
              // Regex fallback for currency
              const match = card.innerText.match(/(\$[\d,.]+|\€[\d,.]+|\£[\d,.]+|[\d,.]+\s?₫|[\d,.]+\s?USD)/);
              if (match) item['Price'] = match[0];
            }

            // Description / Snippet
            const desc = card.querySelector('p, [class*="desc"], [class*="detail"], [class*="snippet"]');
            if (desc) item['Description'] = cleanText(desc.innerText);

            // Image
            const img = card.querySelector('img[src]');
            if (img && img.src && !img.src.startsWith('data:')) item['Image_URL'] = img.src;

            // Rating
            const rating = card.querySelector('[class*="rating"], [class*="star"], [aria-label*="star"], [aria-label*="rating"]');
            if (rating) item['Rating'] = cleanText(rating.getAttribute('aria-label') || rating.innerText);

            // If empty object, take full text
            if (Object.keys(item).length === 0) {
              const fullText = cleanText(card.innerText);
              if (fullText.length > 5) item['Content'] = fullText;
            }

            if (Object.keys(item).length > 0) {
              items.push(item);
            }
          });

          if (items.length >= 3) {
            // Find unified headers
            const allKeys = new Set();
            items.forEach(it => Object.keys(it).forEach(k => allKeys.add(k)));
            const headers = Array.from(allKeys);

            const rows = items.map(it => headers.map(h => it[h] || ''));

            detected.push({
              name: `Repeating List (${items.length} items)`,
              headers: headers,
              rows: rows
            });
          }
        }
      }
    });

    // Return the list with the most data or best score
    detected.sort((a, b) => (b.rows.length * b.headers.length) - (a.rows.length * a.headers.length));
    return detected.slice(0, 3);
  }

  function extractContacts() {
    const text = document.body ? document.body.innerText : '';
    
    // Email regex
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    const emails = Array.from(new Set(text.match(emailRegex) || [])).filter(e => !e.endsWith('.png') && !e.endsWith('.jpg'));

    // Phone regex
    const phoneRegex = /(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}/g;
    const rawPhones = text.match(phoneRegex) || [];
    const phones = Array.from(new Set(rawPhones.map(p => p.trim()))).filter(p => p.length >= 8 && p.length <= 20);

    const contactRows = [];
    const maxLen = Math.max(emails.length, phones.length);
    for (let i = 0; i < maxLen; i++) {
      contactRows.push([
        emails[i] || '',
        phones[i] || '',
        window.location.hostname
      ]);
    }

    return {
      emails: emails,
      phones: phones,
      headers: ['Email', 'Phone Number', 'Source Domain'],
      rows: contactRows
    };
  }

  function cleanText(txt) {
    if (!txt) return '';
    return txt.replace(/\s+/g, ' ').trim();
  }
})();
