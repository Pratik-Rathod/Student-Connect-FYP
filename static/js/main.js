$(document).ready(function () {
  $(".vote").change(function () {
    console.log()
    var temp  = $(this).attr('name')
    // $(this).parent().parent().children('label').eq(1).children('input').prop('checked', false)
     $("input[name="+temp+"]").not(this).prop('checked', false);
  
    }); 
});


// $('.vote').click(function () {
//   alert(0)
//   var catid;
//   catid = $(this).attr("data-catid");
//   $.ajax(
//     {
//       type: "GET",
//       url: "/vote",
//       data: {
//         post_id: catid
//       },
//       success: function (data) {
//         $('#vote' + catid).remove();
//       }
//     })
// });



(function () {
  'use strict'
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
})()



