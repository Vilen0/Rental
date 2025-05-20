document.addEventListener('DOMContentLoaded', () => {
    console.log('Attempting to load sorting.js');
    console.log('Sorting script loaded');
    console.log('Document readyState:', document.readyState);

    // Find the table with id="bookingTable"
    const table = document.getElementById('bookingTable');
    if (!table || table.tagName.toLowerCase() !== 'table') {
        console.error('Table #bookingTable not found or not a <table> element:', table);
        return;
    }
    console.log('Found table:', table);

    const tbody = table.querySelector('tbody');
    if (!tbody) {
        console.error('tbody not found in table#bookingTable');
        return;
    }
    console.log('Found tbody:', tbody);

    const headers = table.querySelectorAll('thead th[data-sort]');
    console.log('Found headers:', headers.length, Array.from(headers).map(h => h.dataset.sort));

    if (headers.length === 0) {
        console.warn('No sortable headers found');
        return;
    }

    headers.forEach(th => {
        th.style.cursor = 'pointer';
    });

    table.addEventListener('click', function(e) {
        const th = e.target.closest('th[data-sort]');
        if (!th) {
            console.log('Click ignored, not a sortable header:', e.target);
            return;
        }

        console.log('Clicked header:', th.dataset.sort, e.target);
        const column = th.dataset.sort;
        const isAsc = !th.classList.contains('sort-asc');
        const rows = Array.from(tbody.querySelectorAll('tr')).filter(row => row.style.display !== 'none');
        console.log('Visible rows:', rows.length);

        if (rows.length === 0) {
            console.error('No rows to sort');
            return;
        }

        headers.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            const icon = header.querySelector('i');
            if (icon) icon.className = 'bi';
        });

        th.classList.add(isAsc ? 'sort-asc' : 'sort-desc');
        const thIcon = th.querySelector('i');
        if (thIcon) thIcon.className = isAsc ? 'bi bi-sort-up' : 'bi bi-sort-down';

        const cellIndex = Array.from(th.parentElement.children).indexOf(th);
        console.log('Cell index:', cellIndex);

        rows.sort((a, b) => {
            const aCell = a.cells[cellIndex];
            const bCell = b.cells[cellIndex];
            if (!aCell || !bCell) {
                console.error(`Cell not found for column ${column}, index ${cellIndex}`);
                return 0;
            }
            let aValue = aCell.dataset.sortValue || aCell.textContent.trim();
            let bValue = bCell.dataset.sortValue || bCell.textContent.trim();
            if (!aCell.dataset.sortValue) {
                console.warn(`No sort value for ${column} in row:`, aCell.textContent);
            }
            console.log(`Comparing ${column}: "${aValue}" vs "${bValue}"`);

            if (!aValue && !bValue) return 0;
            if (!aValue) return isAsc ? 1 : -1;
            if (!bValue) return isAsc ? -1 : 1;

            if (column === 'total_price') {
                aValue = parseFloat(aValue) || 0;
                bValue = parseFloat(bValue) || 0;
                return isAsc ? aValue - bValue : bValue - aValue;
            } else if (column === 'start_date' || column === 'end_date') {
                aValue = aValue ? new Date(aValue) : new Date(0);
                bValue = bValue ? new Date(bValue) : new Date(0);
                if (isNaN(aValue.getTime())) {
                    console.warn(`Invalid date for ${column}: ${aValue}`);
                    aValue = new Date(0);
                }
                if (isNaN(bValue.getTime())) {
                    console.warn(`Invalid date for ${column}: ${bValue}`);
                    bValue = new Date(0);
                }
                console.log('Date parsing:', aValue, bValue);
                return isAsc ? aValue - bValue : bValue - aValue;
            } else {
                return isAsc ? aValue.localeCompare(bValue, 'ru') : bValue.localeCompare(aValue, 'ru');
            }
        });

        console.log('Rows before sort:', rows.map(row => row.cells[cellIndex].dataset.sortValue || row.cells[cellIndex].textContent.trim()));

        console.log('Table innerHTML before:', tbody.innerHTML.substring(0, 100));
        tbody.innerHTML = '';
        console.log('Table innerHTML after clear:', tbody.innerHTML);
        rows.forEach(row => tbody.appendChild(row));
        console.log('Table innerHTML after append:', tbody.innerHTML.substring(0, 100));
        console.log('Table updated, sorted by:', column, isAsc ? 'ASC' : 'DESC');
    });
});