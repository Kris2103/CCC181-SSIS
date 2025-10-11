
// Initialize DataTable (Vanilla JS, DataTables 2.x)
document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('#data-table');

    new DataTable(table, {
        searchable: true,         // enable search box
        sortable: true,           // enable sorting
        perPage: 5,               // rows per page
        perPageSelect: [5, 10, 25], // rows per page dropdown
        columns: Array.from(table.querySelectorAll('th')).map((th, index, arr) => ({
            sortable: index !== arr.length - 1 // disable sort on last column
        }))
    });

    table.style.visibility = 'visible';
});


    // Populate Edit Modal
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('edit-id-number').value = this.dataset.idNumber;
            document.getElementById('edit-first-name').value = this.dataset.firstName;
            document.getElementById('edit-last-name').value = this.dataset.lastName;
            document.getElementById('edit-gender').value = this.dataset.gender;
            document.getElementById('edit-year-level').value = this.dataset.yearLevel;
            document.getElementById('edit-program-code').value = this.dataset.programCode;
        });
    });

    // Populate Delete Modal
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('delete-id-number').value = this.dataset.idNumber;
        });

});
