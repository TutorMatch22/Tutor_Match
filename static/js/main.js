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

    // Toggle dropdown visibility
    function toggleDropdown() {
        document.getElementById("myDropdown").classList.toggle("show");
    }
    
    // Close the dropdown if clicked outside
    window.onclick = function (event) {
        if (!event.target.matches('.dropbtn')) {
            let dropdowns = document.getElementsByClassName("dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                let openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
                }
            }
        }
    }

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

    document.getElementById('sort-by').addEventListener('change', function() {
        const sortBy = this.value;
        const urlParams = new URLSearchParams(window.location.search);
    
        // Update the `sort_by` parameter without removing existing filters
        urlParams.set('sort_by', sortBy);
    
        // Redirect to the updated URL with all current filters and the new sort option
        window.location.href = `${window.location.pathname}?${urlParams.toString()}`;
    });
    
});


// console.log("JavaScript file is linked and running!");
