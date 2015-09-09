/* Javascript for MyXBlock. */
function MyXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }
    function update(result){
        console.log(result)
        window.location.reload(true);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var studiosubmit = runtime.handlerUrl(element, 'studio_submit');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });
 
    $('.save-button', element).bind('click', function(){
        var params = { "src": $('input[name=src]', element).val()};
        
        $.ajax({
              type:"POST",
              url:studiosubmit,
              data: JSON.stringify(params),
              success:update
             });
       
           
   });

    $('.cancle-button', element).bind('click', function(){
        console.log("cancel");
         runtime.notify('cancel', {});
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
