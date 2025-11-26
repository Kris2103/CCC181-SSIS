$(document).ready(function() {
    // Auto-fade for flash messages
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 3000);

    let studentTable; 
    // Student Table Initialization (Custom Search Logic & Custom Sorting)
    if ($('#student-table').length) { 
        studentTable = new DataTable('#student-table', {
            paging: true,
            searching: true,
            ordering: true,
            lengthMenu: [ [5, 10, 25, -1], [5, 10, 25, "All"] ],
            pageLength: 10,
            stateSave: true,
            
            language: {
                search: "",
                searchPlaceholder: "Search Students..." 
            },

            columnDefs: [
                { orderable: false, targets: [0, -1] } 
            ]
        });
        $('#student-table').css('visibility', 'visible');
        const customFilterContent = $('#custom-filter-container').children().first(); 
        const dtSearchWrapper = $('#student-table_wrapper').find('.dt-search'); 
        const dtSearchInput = dtSearchWrapper.find('input[type="search"]');

        if (dtSearchWrapper.length) {
            dtSearchWrapper.prepend(customFilterContent); 
            dtSearchWrapper.find('label[for^="dt-search-"]').hide(); 
            dtSearchWrapper.addClass('d-flex align-items-center gap-0');
            customFilterContent.show(); 
        }

        const searchField = $('#student-table_wrapper').find('.dt-search input[type="search"]'); 
        const filterDropdown = $('#searchByFilterStudent'); 

        // Bind Custom Search Logic
        function applyStudentSearch() {
            if (!studentTable) return; 

            const query = searchField.val();
            const columnIndex = filterDropdown.val();

            studentTable.columns().search('');

            if (columnIndex === '-1') {
                // All field Search
                studentTable.search(query).draw();
            } else {
                // Column Search (targets specific column index)
                studentTable
                    .column(parseInt(columnIndex)) 
                    .search(query)
                    .draw();
            }
        }

        searchField.off('keyup.dt search.dt input.dt'); // Detach default global search
        searchField.on('keyup change', applyStudentSearch);

        filterDropdown.on('change', function() {
            searchField.trigger('keyup'); // Re-run search when column selection changes
        });
    }

    let programTable; 
    // Program Table Initialization
    if ($('#program-table').length) { 
        programTable = new DataTable('#program-table', {
            paging: true,
            searching: true,
            ordering: true,
            lengthMenu: [ [5, 10, 25, -1], [5, 10, 25, "All"] ],
            pageLength: 10,
            stateSave: true,

            language: {
                search: "",
                searchPlaceholder: "Search Programs..."
            },
            columnDefs: [
                { orderable: false, targets: [-1] } 
            ]
        });

        $('#program-table').css('visibility', 'visible');
        const customFilterContent = $('#custom-filter-program-container').children().first(); 
        const dtSearchWrapper = $('#program-table_wrapper').find('.dt-search'); 
        const searchField = dtSearchWrapper.find('input[type="search"]'); 
        const filterDropdown = $('#searchByFilterProgram'); 

        if (dtSearchWrapper.length) {
            dtSearchWrapper.prepend(customFilterContent); 
            dtSearchWrapper.find('label[for^="dt-search-"]').hide(); 
            dtSearchWrapper.addClass('d-flex align-items-center gap-0'); 
            customFilterContent.show(); 
        }

        // Bind Custom Search Logic
        function applyProgramSearch() {
            if (!programTable) return; 

            const query = searchField.val();
            const columnIndex = filterDropdown.val();

            programTable.columns().search('');

            if (columnIndex === '-1') {
                programTable.search(query).draw();
            } else {
                programTable
                    .column(parseInt(columnIndex)) 
                    .search(query)
                    .draw();
            }
        }
        searchField.off('keyup.dt search.dt input.dt');
        searchField.on('keyup change', applyProgramSearch);

        filterDropdown.on('change', function() {
            searchField.trigger('keyup');
        });
    }

    let collegeTable; 
    // College Table Initialization
    if ($('#college-table').length) { 
        collegeTable = new DataTable('#college-table', {
            paging: true,
            searching: true,
            ordering: true,
            lengthMenu: [ [5, 10, 25, -1], [5, 10, 25, "All"] ],
            pageLength: 10,
            stateSave: true,
            
            language: {
                search: "", 
                searchPlaceholder: "Search Colleges..." 
            },
            columnDefs: [
                { orderable: false, targets: [-1] } 
            ]
        });

        $('#college-table').css('visibility', 'visible');
        const customFilterContent = $('#custom-filter-college-container').children().first(); 
        const dtSearchWrapper = $('#college-table_wrapper').find('.dt-search'); 
        const searchField = dtSearchWrapper.find('input[type="search"]'); 
        const filterDropdown = $('#searchByFilterCollege'); 

        if (dtSearchWrapper.length) {
            dtSearchWrapper.prepend(customFilterContent); 
            dtSearchWrapper.find('label[for^="dt-search-"]').hide(); 
            dtSearchWrapper.addClass('d-flex align-items-center gap-0'); 
            customFilterContent.show(); 
        }

        // Bind Custom Search Logic
        function applyCollegeSearch() {
            if (!collegeTable) return; 

            const query = searchField.val();
            const columnIndex = filterDropdown.val();

            collegeTable.columns().search(''); // Clear all previous column filters

            if (columnIndex === '-1') {
                collegeTable.search(query).draw();
            } else {
                // Column Search (targets specific column index)
                collegeTable
                    .column(parseInt(columnIndex)) 
                    .search(query)
                    .draw();
            }
        }

        // 3. Attach Listeners
        searchField.off('keyup.dt search.dt input.dt'); // Detach default global search
        searchField.on('keyup change', applyCollegeSearch);

        filterDropdown.on('change', function() {
            searchField.trigger('keyup');
        });
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
        dropdownParent: $('#registerStudentModal').find('.modal-body'),
        width: '100%',
        placeholder: "Select Program",
        allowClear: true
    });

    $('#edit-program-code').select2({
        dropdownParent: $('#editStudentModal').find('.modal-body'),
        width: '100%',
        placeholder: "Select Program",
        allowClear: true
    });

    // =========================
    // Live image preview
    // =========================
    function previewImage(input, imgId) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $(`#${imgId}`).attr('src', e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#photo_file_register').on('change', function() {
        previewImage(this, 'register-current-photo');
    });

    $('#edit-photo-file').on('change', function() {
        previewImage(this, 'edit-current-photo');
    });

    // --- Upload to backend ---
    async function uploadPhoto(buttonId, formId, imgId, hiddenFieldId) {
        $(`#${buttonId}`).on('click', async function(e) {
            e.preventDefault();

            const form = document.getElementById(formId);
            const fileInput = form.querySelector('input[type="file"]');
            if (!fileInput.files[0]) return alert("Please select a file.");

            const idNumberInput = form.querySelector('input[name="id_number"]');
            const idNumber = idNumberInput.value;
            if (!/^\d{4}-\d{4}$/.test(idNumber)) {
                return alert("Enter a valid Student ID first (YYYY-NNNN).");
            }

            const formData = new FormData();
            formData.append('photo_file', fileInput.files[0]);
            formData.append('id_number', idNumber);

            try {
                const response = await fetch('/students/upload_photo', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    alert("Photo uploaded successfully!");
                    $(`#${imgId}`).attr('src', data.url);
                    $(`#${hiddenFieldId}`).val(data.url);
                } else {
                    alert("Upload failed: " + data.message);
                }
            } catch (err) {
                alert("Upload error: " + err.message);
            }
        });
    }

    // Initialize upload buttons
    uploadPhoto('btn-register-upload-photo', 'register-photo-upload-form', 'register-current-photo', 'register-profile-picture-url');
    uploadPhoto('btn-upload-photo', 'photo-upload-form', 'edit-current-photo', 'edit-profile-picture-url');
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
        modal.find('#edit-college-code-text').val(data.code || "");     // text input
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

        // Default URL is needed for the preview if no custom photo exists
        const defaultPhotoUrl = modal.find('#edit-current-photo').attr('data-default-url'); 
        const photoUrl = data.profilePictureUrl || defaultPhotoUrl;

        // jQuery converts data-id-number to data.idNumber, etc.
        modal.find('#edit-id-number').val(data.idNumber || "");
        modal.find('#edit-first-name').val(data.firstName || "");
        modal.find('#edit-last-name').val(data.lastName || "");
        modal.find('#edit-gender').val(data.gender || "");
        modal.find('#edit-year-level').val(data.yearLevel || "");
        modal.find('#edit-program-code').val(data.programCode || "").trigger('change');

        // --- PHOTO FIELDS ---
        modal.find('#edit-current-photo').attr('src', photoUrl);
        modal.find('#edit-profile-picture-url').val(photoUrl);
        modal.find('#photo-upload-id-number').val(data.idNumber || "");
        modal.find('#edit-photo-file').val('');
    });

    $('#registerStudentModal').on('show.bs.modal', function() {
        const modal = $(this);
        const defaultPhoto = modal.find('#register-current-photo').attr('data-default-url');

        modal.find('form')[0].reset();
        modal.find('#register-current-photo').attr('src', defaultPhoto);
        modal.find('#program_code').val(null).trigger('change');
        modal.find('form').removeClass('was-validated');
    });

    $('#deleteStudentModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        if (!button.length) return;
        // Correctly get 'idNumber' from 'data-id-number' attribute
        const idNumber = button.data('idNumber') || "";
        // Correctly find the input with id '#delete-id-number'
        $(this).find('#delete-id-number').val(idNumber);
    });