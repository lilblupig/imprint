$( document ).ready(function() {

    /* Have form focus set to first field on input pages */
    $( "#username, #name" ).focus();

    /* Allow form submit on enter where no recaptcha */
    $( ".submit-listen" ).keydown(function(event) {
        if (event.key === "Enter") {
            console.log("Enter was pressed")
            $( "#submit" ).click();
            return false;
        }
    })

  });

/* Location getter for Maps */
  const filterBtn = document.getElementById("filter-btn");

  filterBtn.addEventListener("click", function(event) {
      console.log("Filter chosen");
  })