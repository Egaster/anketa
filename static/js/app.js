$(function(){
    /*Smooth Scroll*/
    $("[data-scroll]").on("click", function(event){
        event.preventDefault();

        var blockId = $(this).data('scroll'),
            blockOffset = $(blockId).offset().top;

        $("html, body").animate({
            scrollTop: blockOffset
        }, 550);
    });

    /*Collapse*/
    // $("[data-collapse]").on("click", function(event) {
    //     event.preventDefault();
    
    //     var $this = $(this),
    //         blockId = $this.data('collaps');
        
    //     $this.toggleClass("active");
        
    //     if ($this.hasClass("active")) {
    //         $(blockId).slideDown();
    //     } else {
    //         $(blockId).slideUp();
    //     }
    // });
});

