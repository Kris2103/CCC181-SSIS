$(document).ready(function() {
    // Auto-fade for flash messages
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 3000);

    // DataTables init
    if ($('#data-table').length) {
        new DataTable('#data-table', {
            paging: true,
            searching: true,
            ordering: true,
            lengthMenu: [ [5, 10, 25, -1], [5, 10, 25, "All"] ],
            pageLength: 10,
            stateSave: true,

            columnDefs: [
                { orderable: false, targets: -1 }
            ]
        });

        $('#data-table').css('visibility', 'visible');
    }
// --- INITIALIZE SELECT2 FOR PROGRAM MODALS ---

    // Initialize Select2 for the Add Program Modal
    $('#add-college-code').select2({
        dropdownParent: $('#addProgramModal'),
        tags: true,
        width: '100%',
        placeholder: "Select or type a college code",
        minimumResultsForSearch: 0
    });

    // Initialize Select2 for the Edit Program Modal
    $('#edit-college-code').select2({
        dropdownParent: $('#editProgramModal'),
        tags: true,
        width: '100%',
        placeholder: "Select or type a college code",
        minimumResultsForSearch: 0
    });

        // Student Modals (Program dropdown)
    $('#program_code').select2({
        dropdownParent: $('#registerStudentModal'),
        width: '100%',
        placeholder: "Select Program",
        allowClear: true
    });

    $('#edit-program-code').select2({
        dropdownParent: $('#editStudentModal'),
        width: '100%',
        placeholder: "Select Program",
        allowClear: true
    });

    // Auto-open Select2 dropdown when field is focused
    $('#add-college-code, #edit-program-college-code').on('focus', function (e) {
        $(this).select2('open');
    });


    // == COLLEGE MODALS ==
    $('#editCollegeModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button || !button.length) return;

        const data = button.data(); // expects data-code and data-name
        const modal = $(this);

        // Populate fields
        modal.find('#edit-original-college-code').val(data.code || ""); // hidden original code
        modal.find('#edit-college-code-text').val(data.code || "");    // text input
        modal.find('#edit-college-name').val(data.name || "");          // college name input
    });

    $('#deleteCollegeModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button || !button.length) return;
        const code = button.data('code') || "";
        $(this).find('#delete-college-code').val(code);
    });

    // == PROGRAM MODALS ==
    $('#editProgramModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button.length) return;

        const programCode = button.data('program-code');
        const programName = button.data('program-name');
        const collegeCode = button.data('college-code');

        const modal = $(this);

        modal.find('#edit-original-code').val(programCode);
        modal.find('#edit-program-code-text').val(programCode);
        modal.find('#edit-program-name').val(programName);
        
        // Set the Select2 value correctly and trigger change
        modal.find('#edit-college-code').val(collegeCode).trigger('change');
    });

    $('#deleteProgramModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button.length) return;
        const code = button.data('code');
        $(this).find('#delete-program-code').val(code);
    });

    // == STUDENT MODALS ==
    $('#editStudentModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button.length) return;

        const data = button.data();
        const modal = $(this);

        // jQuery converts data-id-number to data.idNumber, etc.
        modal.find('#edit-id-number').val(data.idNumber || "");
        modal.find('#edit-first-name').val(data.firstName || "");
        modal.find('#edit-last-name').val(data.lastName || "");
        modal.find('#edit-gender').val(data.gender || "");
        modal.find('#edit-year-level').val(data.yearLevel || "");
        modal.find('#edit-program-code').val(data.programCode || "").trigger('change');
    });

    $('#deleteStudentModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button.length) return;
        // Correctly get 'idNumber' from 'data-id-number' attribute
        const idNumber = button.data('idNumber') || "";
        // Correctly find the input with id '#delete-id-number'
        $(this).find('#delete-id-number').val(idNumber);
    });
});