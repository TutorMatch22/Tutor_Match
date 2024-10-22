$(document).ready(function(){
    console.log("JavaScript file is linked and running!");
    
    $('.fa-bars').click(function(){
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('nav-toggle');
    });

    $(window).on('scroll load', function(){
        $('.fa-bars').removeClass('fa-times');
        $('.navbar').removeClass('nav-toggle');

        if($(window).scrollTop() > 30) {
            $('header').addClass('header-active');
        } else {
            $('header').removeClass('header-active');
        }
    });

    // Show the search arrow when search bar is not empty
    $('#keyword').on('input', function() {
        const inputVal = $(this).val();
        if (inputVal.trim() !== '') {
            $('#search-arrow').show(); 
        } else {
            $('#search-arrow').hide(); 
        }
    });

    // Click event for the search arrow
    $('#search-arrow').on('click', function(event) {
        event.preventDefault(); // Prevent any default action
        $('#tutor-search-form').submit(); // Submit the form
    });

    // Add the Enter key submission handler for the search bar in find_tutors.html
    $('#tutor-search-form').on('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); 
            this.submit(); 
        }
    });

    // Ensure all fields are filled when submitting Filter Tutors button
    function validateFilterForm() {
        const subject = document.getElementById('subject').value;
        const rating = document.getElementById('rating').value;
        const startTime = document.getElementById('start_time').value;
        const endTime = document.getElementById('end_time').value;
    
        // Check if all fields are filled for the filter form
        if (!subject || !rating || !startTime || !endTime) {
            alert("Please fill out all fields in the filter form.");
            return false; // Prevent form submission
        }
    
        return true; // Allow form submission
    };    
});


// console.log("JavaScript file is linked and running!");
